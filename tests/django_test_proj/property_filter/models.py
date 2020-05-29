from django.db import models

# Create your models here.

class NumberClass(models.Model):
    number = models.IntegerField(null=True)

    @property
    def prop_number(self):
        return self.number

    def __str__(self):
        return F'{self.number}'
