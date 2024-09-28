from django import forms

class CVUploadForm(forms.Form):
    file = forms.FileField(label='Upload CV')
    job_description = forms.CharField(widget=forms.Textarea, label="Job Description", required=True)

