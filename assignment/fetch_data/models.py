from django.db import models

# Create your models here.

class Metrics(models.Model):
    date = models.DateField()
    place = models.CharField(max_length = 10)
    Tmax = models.DecimalField(max_digits = 4, decimal_places = 1, null = True, blank = True)
    Tmin = models.DecimalField(max_digits = 4, decimal_places = 1, null = True, blank = True)
    Rainfall = models.DecimalField(max_digits = 4, decimal_places = 1, null = True, blank = True)

    class Meta:
        unique_together = ('date', 'place')

    def __str__(self):
        return self.place + ' ' + str(self.date)
