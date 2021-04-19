from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class GenericManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None
