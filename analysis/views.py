from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from models import *
from forms import SampleAnnotationForm
from collections import defaultdict
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
import itertools
import re
from django.template import RequestContext, loader
from django.http import HttpResponse


@login_required
def index(request):
	return render(request, 'analysis/index.html', {})


def check_project_exists(project_id):
	"""
	Returns a Project object or None
	"""
	try:
		existing_project = Project.objects.get(ilab_id = project_id)
	except Project.DoesNotExist:
		return None
	return existing_project


@login_required
def add_new_project(request):
	if request.method == 'POST':
		submitted_project_id = request.POST.get('project_id')
		existing_project = check_project_exists(submitted_project_id)

		already_existed = False
		success = False
		if existing_project:

			if request.user in existing_project.user.all():
				message = "The project (%s) was previously added to your user profile." % existing_project.ilab_id
				already_existed = True
			else:

				# if this is the first user being added to a project, then populate the Sample table.  Otherwise, the information is already there.
				if len(existing_project.user.all()) == 0:
					populate_sample_info(existing_project)

				existing_project.user.add(request.user)
				message = "The project (%s) has been added to your user profile.  You may now perform analyses on this project." % existing_project.ilab_id
				success = True
		else:
			message = "The specified project id (%s) does not exist.  Please check that it was typed correctly." % submitted_project_id

		return render(request, 'analysis/add_project.html', {'success': success, 'message': message, 'queried': True, 'already_existed':already_existed})	
	else:
		print 'get'
	return render(request, 'analysis/add_project.html', {})



@login_required
def create_analysis(request):

	if request.method == 'POST':

		if request.POST.get('analysis_pk'):
			analysis_pk = request.POST.get('analysis_pk')
			analysis_obj = Analysis.objects.get(pk = analysis_pk)
			analysis_samples = AnalysisSample.objects.filter(analysis = analysis_obj)
			analysis_samples = sorted(analysis_samples, key=lambda s: s.sample.name.lower())
		else:
			selected_project_id = request.POST.get('selected_project_id')
			custom_name = request.POST.get('analysis_name')
			new_analysis = Analysis()
			new_analysis.user = request.user
			new_analysis.project = check_project_exists(selected_project_id)
			new_analysis.common_name = custom_name
			new_analysis.save()
			analysis_pk = new_analysis.pk
			#now that analysis exists, port over the samples from the project into the AnalysisSample table
			all_samples_for_project = get_samples_for_project(selected_project_id)
			analysis_samples = []
			for base_sample in all_samples_for_project:
				analysis_sample = AnalysisSample()
				analysis_sample.sample = base_sample
				analysis_sample.analysis = new_analysis
				analysis_sample.save()
				analysis_samples.append(analysis_sample)
		forms = []
		for i,s in enumerate(analysis_samples):
			forms.append(SampleAnnotationForm(
				prefix = str(i),
				instance = s
			))

		return render(request,'analysis/sample_entry.html',{'forms':forms, 'analysis_pk':analysis_pk})


		#return redirect(reverse('annotate_samples', args=(selected_project_id,)))
	else:
		context = {}
		associated_projects = Project.objects.filter(user = request.user)
		if len(associated_projects) > 0:
			context['user_has_projects'] = True
			context['all_projects'] = [p.ilab_id for p in associated_projects]	
		else:
			context['user_has_projects'] = False
		return render(request, 'analysis/create_analysis.html', context)
	



@login_required
def annotate_samples(request):
	if request.method == 'POST':

		analysis_pk = request.POST.get('analysis_pk')
		analysis_obj = Analysis.objects.get(pk = analysis_pk)
		analysis_samples = AnalysisSample.objects.filter(analysis = analysis_obj)
		analysis_samples = sorted(analysis_samples, key=lambda s: s.sample.name.lower())

		#num_samples = int(request.POST.get('num_samples'))
		#project_id = request.POST.get('project_id')

		forms = [SampleAnnotationForm(request.POST, prefix=str(i), instance=analysis_samples[i]) for i in range(len(analysis_samples))]

		if all([f.is_valid() for f in forms]):
			for f in forms:
				f.save()
			cmap, skipped_sample_names = prepare_annotation_summary(analysis_samples)
			print cmap
			return render(request, 'analysis/sample_annotation_summary.html', {'condition_to_sample_map': cmap, 'analysis_pk':analysis_pk, 'skipped_samples':skipped_sample_names})
		else:
			return render(request,'analysis/sample_entry.html',{'forms':forms, 'analysis_pk':analysis_pk})


@login_required
def specify_contrasts(request):
	if request.method == 'POST':
		analysis_pk = request.POST.get('analysis_pk')
		groups = get_groups(analysis_pk)
		context = {}
		context['analysis_pk'] = analysis_pk
		context['all_conditions'] = list(groups)
		return render(request, 'analysis/contrasts.html', context)


def get_groups(analysis_pk):
	analysis_obj = Analysis.objects.get(pk = analysis_pk)
	analysis_samples = AnalysisSample.objects.filter(analysis = analysis_obj)
	groups = set()
	for sample in analysis_samples:
		if sample.is_used:
			groups.add(sample.condition)
	return groups

def get_samples_for_project(project_id):
	selected_project = check_project_exists(project_id)
	if selected_project:
		project_samples = BaseSample.objects.filter(project=selected_project)
		return sorted(project_samples, key=lambda s: s.name.lower())



@login_required
def view_submitted_analyses(request):

	# views on both the user's analyses AND their associated projects

	this_users_analyses = Analysis.objects.filter(user = request.user)
	print this_users_analyses
	# projects associated with this user:
	associated_projects = Project.objects.filter(user = request.user)
	print associated_projects	
	# now, get analyses associated with those projects
	all_analyses_from_associated_projects = Analysis.objects.filter(project__in=associated_projects)
	print all_analyses_from_associated_projects
	
	user_summaries = AnalysisSummary.objects.filter(analysis__in=this_users_analyses)
	assoc_proj_summaries = AnalysisSummary.objects.filter(analysis__in=all_analyses_from_associated_projects)
	assoc_proj_summaries = assoc_proj_summaries.exclude(pk__in = user_summaries)
	context = {}
	context['user_summaries'] = user_summaries
	context['assoc_proj_summaries'] = assoc_proj_summaries
	return render(request, 'analysis/submitted_analyses.html', context)


@login_required
def submit_analysis(request):
	if request.method == 'POST':

		contrast_pairing_str = request.POST.get('contrast_pairing_str')
		contrast_pairing = [tuple(x.split(',')) for x in contrast_pairing_str.split(';')]
		analysis_pk = request.POST.get('analysis_pk')
		analysis_obj = Analysis.objects.get(pk = analysis_pk)
		project_obj = analysis_obj.project

		if request.user in project_obj.user.all():
				a = AnalysisSummary()
				a.analysis = analysis_obj
				a.command = contrast_pairing_str
				a.save()
				return redirect(reverse('analysis_history'))				
	return redirect(reverse('create_analysis'))


@login_required
def summary(request):
	if request.method == 'POST':
		analysis_pk = request.POST.get('analysis_pk')
		analysis_obj = Analysis.objects.get(pk = analysis_pk)
		analysis_samples = AnalysisSample.objects.filter(analysis = analysis_obj)
		existing_project = analysis_obj.project

		if existing_project and request.user in existing_project.user.all():
			cmap, skipped = prepare_annotation_summary(analysis_samples)

			if request.POST.get('contrast_radio'):
				# this means all pairwise contrasts
				groups = cmap.keys()
				contrast_pairings = set(itertools.combinations(groups, 2))
				print contrast_pairings
			else:
				pattern = r'contrast_[\d]+_condition_\w'
				contrast_keys = []
				for key in request.POST.keys():
					m = re.match(pattern,key)
					if m:
						contrast_keys.append(m.group())
				# sort so the pairs are next to each other in the list (since names were chosen so accomodate this behavior)
				contrast_keys.sort()
				contrast_pairings = []
				for k in range(len(contrast_keys)/2):
					c1 = request.POST.get(contrast_keys[2*k])
					c2 = request.POST.get(contrast_keys[2*k+1])
					if c1 != c2:
						contrast_pairings.append((c1,c2))

			context = {}
			context['condition_to_sample_map'] = cmap
			context['contrast_pairings'] = contrast_pairings 
			context['analysis_pk'] = analysis_pk
			context['skipped_samples'] = skipped
			context['contrast_pairing_str'] = ';'.join([','.join(p) for p in contrast_pairings]) #specially formatted string for passing around
			return render(request, 'analysis/summary.html', context)
				
		else:
			return redirect(reverse('create_analysis'))
	return render(request, 'analysis/summary.html', {'msg':'hi'})


@login_required
def return_analysis_info(request):
	if request.method == 'GET':
		primary_key = request.GET.get('analysis_summary_pk')
		summary = AnalysisSummary.objects.get(pk=primary_key)
		analysis_obj = summary.analysis
		samples = AnalysisSample.objects.filter(analysis = analysis_obj)
		samples = [s for s in samples if s.is_used]

		contrasts = [tuple(x.split(',')) for x in summary.command.split(';')]
		d= {'contrasts':contrasts, 'samples':samples}
                context = RequestContext(request, d)

                my_template = loader.get_template('analysis/modal_body.html')
       	        response = my_template.render(context)
		print response
                return HttpResponse(response)


def populate_sample_info(project):
	"""
	Receives a Project object that is from the Project table.  Gets the sample names (and conditions if they have been set) and populates the Sample table
	"""
	print 'populating sample info'
	samples = mock_sample_get_method_1()
	for s in samples:
		p = BaseSample()
		p.name = s
		p.project = project
		p.save()	



def prepare_annotation_summary(analysis_samples):
	"""
	Maps the groups to the samples- used this instead of defaultdict since the templates would not render those.  Had to create a regular dict anyway.
	"""
	cmap = {}
	skipped = []
	for s in analysis_samples:
		if s.is_used:
			try:
				cmap[s.condition].append(s.sample.name)
			except KeyError:
				cmap[s.condition] = [s.sample.name,]
		else:
			skipped.append(s.sample.name)	
	return cmap, skipped



def mock_sample_get_method_1():
	return ['WT1','WT2','WT3','KO1','KO2','KO3']


def mock_sample_get_method_2():
	sample_ids = ['WT1','WT2','WT3','KO1','KO2','KO3']
	conditions = ['WT','WT','WT','KO','KO','KO']
	return zip(sample_ids, conditions)



