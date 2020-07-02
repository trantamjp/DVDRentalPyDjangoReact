from django.db import models

from .base_model import BaseModel


class Country(BaseModel):
    country_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=50)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'country'
        app_label = 'api'

    def __str__(self):
        return '<Country {} {}>'.format(self.country_id, self.country)
