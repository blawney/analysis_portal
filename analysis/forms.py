from django import forms
from models import AnalysisSample
from django.core.validators import RegexValidator


alphanumeric = RegexValidator(r'^[0-9a-zA-Z\-\_]*$', message = 'Invalid condition identifier- please only user letters, numbers, dash ("-"), and underscore ("_")')

class SampleAnnotationForm(forms.ModelForm):
	condition = forms.CharField(required=False, 
					max_length=50, 
					widget=forms.TextInput(attrs={'class': 'form-control'}))

	def clean(self):
		if self.cleaned_data['is_used']:		
			if self.cleaned_data['condition']:
				try:
					alphanumeric( self.cleaned_data['condition'] )
				except forms.ValidationError as ex:
					self.add_error('condition', forms.ValidationError('Invalid condition identifier- please only user letters, numbers, dash ("-"), and underscore ("_")'))	
			else:
				self.add_error('condition', forms.ValidationError("Enter a condition if you wish to use this sample."))	

		
	class Meta:
		model = AnalysisSample
		fields = ['is_used', 'condition']
		#exclude = ('sample','analysis',)
