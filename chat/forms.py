from django import forms
from .models import MessageImageType


class MessageImageForm(forms.ModelForm):
    class Meta:
        model = MessageImageType
        fields = ['content']
        labels = {'content': ''}
        widgets = {'content': forms.FileInput({'class': 'image-send-button'})}

    def clean_content(self, *args, **kwargs):
        image = self.cleaned_data.get('content')

        return image
