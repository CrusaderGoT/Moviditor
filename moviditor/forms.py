'''build forms here'''
from django import forms
from . models import AudioModel, ImageModel, VideoModel

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)
    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(data, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
    
class FileFieldForm(forms.Form):
    file_field = MultipleFileField()

class AudioForm(forms.ModelForm):
    class Meta:
        model = AudioModel
        fields = ['audio']
        labels = {'audio': 'Select an audio file\n'}

class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['image']
        labels = {'image': 'choose an image to use for the video:'}

class VideoForm(forms.ModelForm):
    class Meta:
        model = VideoModel
        fields = ['video']
        labels = {'video': 'upload a video:'}

