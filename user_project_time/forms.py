from django import forms
from django.utils import timezone


class SetTaskDeadlineForm(forms.Form):
    time_start = forms.DateTimeField(
        label='Начало',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        required=False
    )
    time_end = forms.DateTimeField(
        label='Конец',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        required=False
    )

    def clean_time_end(self):
        time_start = self.cleaned_data['time_start']
        time_end = self.cleaned_data['time_end']
        if time_end is None:
            return time_end

        if time_start is None:
            time_start = timezone.now()

        if (time_end - time_start).total_seconds() <= 0:
            raise forms.ValidationError('Invalid start and end time', code='invalid')
        return time_end