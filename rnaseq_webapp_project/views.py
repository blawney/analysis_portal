from django.core.urlresolvers import reverse
from django.shortcuts import redirect

def home(request):
	if request.user.is_authenticated():
		return redirect('analysis/')
	else:
		return redirect('accounts/login/')
