from django.db import models


class BaseModel(models.Model):

    class Meta:
        abstract = True

    def row2dict(self):
        # pylint: disable=maybe-no-member
        opts = self._meta
        data = {}
        for field in opts.fields:
            data[field.name] = field.value_from_object(self)
        return data
