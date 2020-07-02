from django.db import models

from .base_model import BaseModel


class FilmCategory(BaseModel):
    film = models.ForeignKey('Film', models.DO_NOTHING)
    category = models.ForeignKey('Category', models.DO_NOTHING)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'film_category'
        unique_together = (('film', 'category'),)
        app_label = 'api'

    def __str__(self):
        return '<FilmCategory film_id={} category_id={}>'.format(self.film_id, self.category_id)
