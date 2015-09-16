from django.conf.urls import url
import views


urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^add_new_project/$', views.add_new_project, name = 'add_project'),
	url(r'^create_analysis/$', views.create_analysis, name = 'create_analysis'),
	#url(r'^create_analysis/project_id/(?P<project_id>[\w\-]+)/annotate/$', views.annotate_samples, name = 'annotate_samples'),
	url(r'^create_analysis/specify_contrasts/$', views.specify_contrasts, name = 'specify_contrasts'),
	url(r'^create_analysis/annotation_summary/$', views.annotate_samples, name = 'annotation_summary'),
	url(r'^create_analysis/analysis_summary/$', views.summary, name = 'analysis_summary'),
	url(r'^submit_analysis/$', views.submit_analysis, name = 'submit_analysis'),
	url(r'^analysis_parameters/$', views.return_analysis_info, name = 'get_analysis_params'),
	url(r'^analysis_history/$', views.view_submitted_analyses, name = 'analysis_history'),
]
