
from django import forms
from django.conf import settings
from uuid import uuid4


class UploadFileForm(forms.Form):
    file = forms.FileField()

    def save_file(self) -> str:
        file_to_save = self.cleaned_data['file']
        unique_filename = settings.MEDIA_ROOT / 'uploaded' / f'{uuid4()}.evtx'
        with open(unique_filename, 'wb+') as destination:
            for chunk in file_to_save.chunks():
                destination.write(chunk)
        return unique_filename