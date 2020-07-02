from django.db import models

from .base_model import BaseModel


class Address(BaseModel):
    address_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=20)
    city = models.ForeignKey('City', models.DO_NOTHING)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=20)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'address'
        app_label = 'api'

    def __repr__(self):
        return '<Address {} {} {} -> city_id {}>'.format(self.address_id, self.address, self.address2, self.city_id)
