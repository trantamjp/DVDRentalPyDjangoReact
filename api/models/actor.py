from django.db import models

from .base_model import BaseModel


class Actor(BaseModel):
    actor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    last_update = models.DateTimeField()

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    # Add additional columns into dict which are not in cls._meta.fields
    def row2dict(self):
        d = super().row2dict()
        d['full_name'] = self.full_name
        return d

    class Meta:
        managed = False
        db_table = 'actor'
        app_label = 'api'

    def __str__(self):
        return '<Actor {} {} {}>'.format(self.actor_id, self.first_name, self.last_name)
