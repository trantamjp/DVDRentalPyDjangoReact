from django.db import models

from .base_model import BaseModel


class Category(BaseModel):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'category'
        app_label = 'api'

    def __str__(self):
        return '<Category {} {}>'.format(self.category_id, self.name)
