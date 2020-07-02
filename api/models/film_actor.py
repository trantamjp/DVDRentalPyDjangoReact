from django.db import models

from .base_model import BaseModel


class FilmActor(BaseModel):
    film = models.ForeignKey('Film', models.DO_NOTHING)
    actor = models.ForeignKey('Actor', models.DO_NOTHING)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'film_actor'
        unique_together = (('film', 'actor'),)
        app_label = 'api'

    def __str__(self):
        return '<FilmActor film_id={} actor_id={}>'.format(self.film_id, self.actor_id)
