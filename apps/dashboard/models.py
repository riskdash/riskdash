from django.db import models
from jsonfield import JSONField

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

class CumRF (models.Model):
	date = models.CharField(max_length=100)
	frac = models.FloatField()

	def __unicode__(self):
		return str(self.frac)

class GrangerCausalityConn(models.Model):
	imports = JSONField()

	def __unicode__(self):
		return str(self.imports)

class GrangerRan(models.Model):
	date = models.CharField(max_length=100)
	imports = JSONField()

	def __unicode__(self):
		return str(self.date)

class Qstatswithpvals(models.Model):
	date = models.CharField(max_length=100)
	val = models.FloatField()

	def __unicode__(self):
		return str(self.date)

class AggIlliq(models.Model):
	date = models.CharField(max_length=100)
	val = models.FloatField()

	def __unicode__(self):
		return str(self.date)

class B1Months(models.Model):
	date = models.CharField(max_length=100)
	val = models.FloatField()

	def __unicode__(self):
		return str(self.date)

class B1defIntensity(models.Model):
	date = models.CharField(max_length=100)
	val = models.FloatField()

	def __unicode__(self):
		return str(self.date)