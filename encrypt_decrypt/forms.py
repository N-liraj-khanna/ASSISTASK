from django import forms  
from django.utils.translation import ugettext_lazy as _

class UploadForm(forms.Form):  
    file= forms.FileField(label="Click here to upload")
    
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.label_suffix = ""