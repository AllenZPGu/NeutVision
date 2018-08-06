from django.db import models
from django.contrib.auth.models import User

class Images(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200, null=True)
	count = models.IntegerField(null=True, default=0)
	source = models.CharField(max_length=200, null=True)

	class Meta:
		db_table = 'Images'

class Scores(models.Model):
	id = models.AutoField(primary_key=True)
	scorer = models.ForeignKey(User, models.DO_NOTHING, db_column='scorer', null=True)
	img = models.ForeignKey(Images, models.DO_NOTHING, db_column='img', null=True)
	
	quality = models.CharField(max_length=200, null=True)
	degree = models.CharField(max_length=200, null=True)
	lobe = models.CharField(max_length=200, null=True)
	shape = models.CharField(max_length=200, null=True)
	allothercomments = models.CharField(max_length=200, null=True)

	date = models.DateField(blank=True, null=True)

	class Meta:
		db_table = 'Scores'