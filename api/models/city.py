from django.db import models

from .base_model import BaseModel


class City(BaseModel):
    city_id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=50)
    country = models.ForeignKey('Country', models.DO_NOTHING)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'city'
        app_label = 'api'

    def __repr__(self):
        return '<City {} {} -> country_id {}>'.format(self.city_id, self.city, self.country_id)
