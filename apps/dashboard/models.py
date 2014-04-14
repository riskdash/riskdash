from django.db import models

class SumStatistics (models.Model):
	sector = models.CharField(max_length=100)
	sample_size = models.FloatField()
	ann_mean = models.FloatField()
	ann_sd = models.FloatField()
	minimum = models.FloatField()
	maximum = models.FloatField()
	median = models.FloatField()
	skewness = models.FloatField()
	kurtosis = models.FloatField()
	p1 = models.FloatField()
	p1_value = models.FloatField()
	p2 = models.FloatField()
	p2_value = models.FloatField()
	p3 = models.FloatField()
	p3_value = models.FloatField()

	def __unicode__(self):
		return self.sector
