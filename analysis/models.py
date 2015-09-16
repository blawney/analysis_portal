from django.db import models
from django.contrib.auth.models import User

'''

The database schema is setup so that different users and setup different analyses on the same set of samples in a project.
This way, their sample annotations do not conflict (e.g. they can call the conditions by different identifiers)
Also, it allows samples to be omitted if they want to remove them from an analysis.

It does this by having a simple table of project and samples.  This way, everyone gets the same samples to begin with.
Then, upon initiating an analysis, one can add annotations and choose a subset of those samples to use in a particular analysis

A single user can generate multiple analyses on the same project, and multiple users can work on the same project.

A single user can work on many projects as well (hence ManyToMany field in the Project object)
'''


class Project(models.Model):
	"""
	Holds project identifiers which match iLab project identifiers.
	"""

	ilab_id = models.CharField(max_length = 24, unique = True)
	user = models.ManyToManyField(User, blank=True)

	def __unicode__(self):
		return self.ilab_id


class Analysis(models.Model):
	project = models.ForeignKey(Project)
	user = models.ForeignKey(User, null=True, blank=True, default = None)
	common_name = models.CharField(max_length=100, default=None, blank=True)

	def __unicode__(self):
		return '(' +str(self.project) + '), ' + str(self.user) + ', ' + self.common_name



class AnalysisSummary(models.Model):
	"""
	Holds information about a particular analysis request that was generated
	"""
	
	analysis = models.ForeignKey(Analysis)
	command = models.CharField(max_length=1200)
	start_time = models.DateTimeField(auto_now_add = True)
	finish_time = models.DateTimeField(null=True, default=None, blank=True)
	result_url = models.URLField()
	is_complete = models.BooleanField(default = False)
	has_error = models.BooleanField(default = False)



class BaseSample(models.Model):
	"""
	Holds information about the samples associated with a project
	"""
	
	project = models.ForeignKey(Project)
	name = models.CharField(max_length=128)

	def __unicode__(self):
		return '(' + str(self.project) + '): ' + self.name


class AnalysisSample(models.Model):
	"""
	Holds information about which samples from a project are held in a particular analysis.
	"""
	
	sample = models.ForeignKey(BaseSample)
	analysis = models.ForeignKey(Analysis)
	condition = models.CharField(max_length=50, blank=True, null=True)
	is_used = models.BooleanField(default = True)

	def __unicode__(self):
		return '(' + str(self.analysis) + '): ' + str(self.sample) 


