from django.db import models

from .base_model import BaseModel


class Language(BaseModel):
    language_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'language'
        app_label = 'api'

    def __str__(self):
        return '<Language {} {}>'.format(self.language_id, self.name)
