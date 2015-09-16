from django.contrib import admin
from models import *


class ProjectAdmin(admin.ModelAdmin):
	list_display = ('ilab_id', 'user_info')

	def user_info(self, obj):
		return '\n'.join([u.username for u in obj.user.all()])


class AnalysisSummaryAdmin(admin.ModelAdmin):
	list_display = ('analysis_name', 'project_info', 'user_info', 'command', 'start_time', 'finish_time', 'result_url', 'is_complete', 'has_error')

	def analysis_name(self,obj):
		return obj.analysis.common_name

	def project_info(self, obj):
		return obj.analysis.project.ilab_id

	def user_info(self, obj):
		return obj.analysis.user.username


class AnalysisAdmin(admin.ModelAdmin):
	list_display = ('project_id', 'user_info', 'common_name')

	def user_info(self, obj):
		return obj.user.username

	def project_id(self, obj):
		return obj.project.ilab_id


class AnalysisSampleAdmin(admin.ModelAdmin):
	list_display = ('sample_name','analysis_id','condition', 'is_used')

	def sample_name(self, obj):
		return obj.sample.name

	def analysis_id(self, obj):
		return obj.analysis.pk


class BaseSampleAdmin(admin.ModelAdmin):
	list_display = ('project','name',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(AnalysisSummary, AnalysisSummaryAdmin)
admin.site.register(BaseSample, BaseSampleAdmin)
admin.site.register(AnalysisSample, AnalysisSampleAdmin)
admin.site.register(Analysis, AnalysisAdmin)
