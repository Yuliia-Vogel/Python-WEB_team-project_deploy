# from django import forms
# from .models import UploadedFile

# class UploadFileForm(forms.ModelForm):
#     class Meta:
#         model = UploadedFile
#         fields = ['file']


from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()
