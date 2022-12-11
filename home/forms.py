from django import forms


class StudySessionForm(forms.Form):
    title = forms.CharField()
    location = forms.CharField()
    startTime = forms.DateTimeField(label='Start Time', widget=forms.widgets.DateTimeInput(
        format='%d/%m/%Y %H:%M', attrs={'type': 'datetime-local'}))
    endTime = forms.DateTimeField(label='End Time', widget=forms.widgets.DateTimeInput(
        format='%d/%m/%Y %H:%M', attrs={'type': 'datetime-local'}))
    description = forms.DateTimeField(widget=forms.Textarea())



