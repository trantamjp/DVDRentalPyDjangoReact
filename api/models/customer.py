from django.db import models
from django.db.models import Q, Subquery

from .base_model import BaseModel


class Customer(BaseModel):
    customer_id = models.AutoField(primary_key=True)
    store_id = models.SmallIntegerField()
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=50, blank=True, null=True)
    address = models.ForeignKey('Address', models.DO_NOTHING)
    activebool = models.BooleanField()
    create_date = models.DateField()
    last_update = models.DateTimeField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'
        app_label = 'api'

    def __repr__(self):
        return '<Customer {} {} {} -> address_id {}>'.format(self.customer_id, self.first_name, self.last_name, self.address_id)

    @classmethod
    def datatable_search(cls, args):

        offset = args.get('offset') or 0
        limit = args.get('limit') or 10
        filters = args.get('filters') or {}
        orders = args.get('orders') or []

        # Remove any filter with the empty search value
        filters = [filter for filter in filters if filter.get('value')]

        records_total = Customer.objects.count()

        rs_filters = []
        for filter in filters:
            filter_id = filter.get('id')

            search_value = filter.get('value') or ''

            if filter_id == 'first_name':
                rs_filters.append(Q(first_name__icontains=search_value))
                continue

            if filter_id == 'last_name':
                rs_filters.append(Q(last_name__icontains=search_value))
                continue

            if filter_id == 'activebool':
                rs_filters.append(
                    Q(activebool__exact=(str(search_value) == '1')))
                continue

            if filter_id == 'address.address':
                rs_filters.append(Q(address__address__icontains=search_value) | Q(
                    address__address2__icontains=search_value))
                continue

            if filter_id == 'address.postal_code':
                rs_filters.append(
                    Q(address__postal_code__icontains=search_value))
                continue

            if filter_id == 'address.phone':
                rs_filters.append(Q(address__phone__icontains=search_value))
                continue

            if filter_id == 'address.city.city':
                rs_filters.append(
                    Q(address__city__city__icontains=search_value))
                continue

            if filter_id == 'address.city.country.country':
                rs_filters.append(
                    Q(address__city__country__country__icontains=search_value))
                continue

        rs_filtered = Customer.objects.filter(*rs_filters)

        # Count without limit
        records_filtered = rs_filtered.count()

        order_by = []
        for order in orders:
            order_id = order.get('id')
            order_prefix = '' if order.get('desc') else '-'

            if order_id == 'first_name':
                order_by.append(order_prefix + 'first_name')
                continue

            if order_id == 'last_name':
                order_by.append(order_prefix + 'last_name')
                continue

            if order_id == 'activebool':
                order_by.append(order_prefix + 'activebool')
                continue

            if order_id == 'address.address':
                order_by.append(order_prefix + 'address__address')
                order_by.append(order_prefix + 'address__address2')
                continue

            if order_id == 'address.postal_code':
                order_by.append(order_prefix + 'address__postal_code')
                continue

            if order_id == 'address.phone':
                order_by.append(order_prefix + 'address__phone')
                continue

            if order_id == 'address.city.city':
                order_by.append(order_prefix + 'address__city__city')
                continue

            if order_id == 'address.city.country.country':
                order_by.append(
                    order_prefix + 'address__city__country__country')
                continue

        final_query = (rs_filtered.order_by(*order_by)[offset: offset+limit]) \
            .select_related('address', 'address__city', 'address__city__country')

        customers = final_query.all()

        customer_list = {
            'records_total': records_total,
            'records_filtered': records_filtered,
            'customers': customers,
        }

        return customer_list
