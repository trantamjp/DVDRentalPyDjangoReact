from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GistIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.db.models import Exists, F, OuterRef, Prefetch, Q
from django.db.models import Value as V
from django.db.models.functions import Cast, Concat
from django.utils.translation import gettext_lazy as _

from ..models import Actor, Category, Language
from .base_model import BaseModel


class Film(BaseModel):

    class Rating(models.IntegerChoices):
        G = 1, _('G')
        PG = 2, _('PG')
        PG_13 = 3, _('PG-13')
        R = 4, _('R')
        NC_17 = 5, _('NC-17')

    film_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    language = models.ForeignKey(Language, models.DO_NOTHING)
    rental_duration = models.SmallIntegerField()
    rental_rate = models.DecimalField(max_digits=4, decimal_places=2)
    length = models.SmallIntegerField(blank=True, null=True)
    replacement_cost = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.IntegerField(choices=Rating.choices)
    last_update = models.DateTimeField()
    special_features = ArrayField(models.TextField(blank=True, null=True))
    fulltext = SearchVectorField(null=False)

    categories = models.ManyToManyField(
        Category, through='FilmCategory',  related_name='films')

    actors = models.ManyToManyField(
        Actor, through='FilmActor',  related_name='films')

    class Meta:
        managed = False
        db_table = 'film'
        indexes = [GistIndex(fields=["fulltext"])]
        app_label = 'api'

    def __repr__(self):
        return '<Film {} {}>'.format(self.film_id, self.title)

    @classmethod
    def datatable_search(cls, args):

        offset = args.get('offset') or 0
        limit = args.get('limit') or 10
        filters = args.get('filters') or {}
        orders = args.get('orders') or []

        # Remove any filter with the empty search value
        filters = [filter for filter in filters if filter.get('value')]

        records_total = Film.objects.count()

        def order_by_for_film(orders):
            order_by = []
            annotates = {}  # to hold any annotate that's required for ordering
            for order in orders:
                order_id = order.get('id')
                order_prefix = '-' if order.get('desc') else ''

                if order_id == 'title':
                    order_by.append(order_prefix + 'title')
                    continue

                if order_id == 'length':
                    order_by.append(order_prefix + 'length')
                    continue

                if order_id == 'rating':
                    rating_as_text = Cast('rating', models.TextField())
                    rating_order = rating_as_text.desc() if order.get(
                        'desc') else rating_as_text.asc()
                    order_by.append(rating_order)
                    continue

                if order_id == 'rental_rate':
                    order_by.append(order_prefix + 'rental_rate')
                    continue

                if order_id == 'language.name':
                    order_by.append(order_prefix + 'language__name')
                    continue

                if order_id == 'actors.full_name':
                    order_by.append(order_prefix + 'actor_list')
                    annotates['actor_list'] = 1
                    continue

                if order_id == 'categories.category':
                    order_by.append(order_prefix + 'category_list')
                    annotates['category_list'] = 1
                    continue

            return order_by, list(annotates.keys())

        rs_filters = []
        for filter in filters:
            filter_id = filter.get('id')

            search_value = filter.get('value')

            if filter_id == 'title':
                rs_filters.append(Q(title__icontains=search_value))
                continue

            if filter_id == 'categories.category':
                rs_filters.append(Exists(Category.objects.filter(
                    filmcategory__film_id=OuterRef('film_id'), name__icontains=search_value)))
                continue

            if filter_id == 'actors.full_name':
                rs_filters.append(Exists(
                    Actor.objects.filter(Q(first_name__icontains=search_value) | Q(
                        last_name__icontains=search_value))
                    .filter(filmactor__film_id=OuterRef('film_id'))
                ))
                continue

            if filter_id == 'length':
                rs_filters.append(Q(length__icontains=search_value))
                continue

            if filter_id == 'rating':
                rs_filters.append(Q(rating__icontains=search_value))
                continue

            if filter_id == 'language.name':
                rs_filters.append(Q(language__name__icontains=search_value))
                continue

            if filter_id == 'rental_rate':
                rs_filters.append(
                    Q(rental_rate__icontains=search_value))
                continue

        rs_filtered = Film.objects.filter(*rs_filters)

        # Count without limit
        records_filtered = rs_filtered.count()

        # populate list of order expressions
        (order_by_for_film, annotate_list) = order_by_for_film(orders)

        # Add annotates for ordering
        if "category_list" in annotate_list:
            sub = Category.objects.filter(filmcategory__film_id=OuterRef('film_id')).values('filmcategory__film_id').annotate(
                category_list=StringAgg('name', delimiter="\t", ordering="name")).values('category_list')
            rs_filtered = rs_filtered.annotate(category_list=sub)

        if "actor_list" in annotate_list:
            sub = Actor.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')).filter(filmactor__film_id=OuterRef('film_id')).values(
                'filmactor__film_id').annotate(actor_list=StringAgg('full_name', delimiter="\t", ordering=["first_name", "last_name"])).values('actor_list')
            rs_filtered = rs_filtered.annotate(actor_list=sub)

        final_query = (rs_filtered.order_by(*order_by_for_film)[offset: offset+limit]) \
            .select_related('language') \
            .prefetch_related(
                # Category
                Prefetch('categories',
                         queryset=Category.objects.order_by("name")),
                # Actor
                Prefetch('actors', queryset=Actor.objects.order_by(
                    "first_name", "last_name")),
        )

        films = final_query.all()

        film_list = {
            'records_total': records_total,
            'records_filtered': records_filtered,
            'films': films,
        }

        return film_list
