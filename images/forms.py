from django import forms
from .models import Image
from django.utils.text import slugify
from urllib import request
from django.core.files.base import ContentFile

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title','url','description']
        widgets = {
            'url':forms.HiddenInput
        }
    
    def clean_url(self):
        url = self.cleaned_data['url']
        extension = url.rsplit('.',1)[1]
        valid_extensions = ['png','jpeg','jpg']

        if extension not in valid_extensions:
            print('>>>> bad url')
            raise forms.ValidationError('Image type not accepted')
        return url
    
    def save(self,force_update=False,force_insert=False,commit=True):
        new_image = super(ImageCreateForm,self).save(commit=False)
        url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(new_image.title),url.rsplit('.',1)[1])

        response = request.urlopen(url)
        new_image.image.save(image_name,ContentFile(response.read()),save=False)
        
        if commit:
            new_image.save()
        return new_image
