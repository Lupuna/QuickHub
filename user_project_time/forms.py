from django import forms


class SetTaskDeadlineForm(forms.Form):
    time_start = forms.DateTimeField(widget=forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'datetime-local'
    }))
    time_end = forms.DateTimeField(widget=forms.DateInput(attrs={
        'class': 'form-control',
        'type': 'datetime-local'
    }))

    def clean_time_end(self):
        time_start = self.cleaned_data['time_start']
        time_end = self.cleaned_data['time_end']
        if (time_end - time_start).total_seconds() <= 0:
            raise forms.ValidationError('Invalid start and end time', code='invalid')
        return time_end