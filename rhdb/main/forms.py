from django import forms


class SearchForm(forms.Form):
    content = forms.CharField(required=False, label='Искать',
                              max_length=200)
    region = forms.CharField(required=False, label='Регион',
                             max_length=50)
    district = forms.CharField(required=False, label='Район',
                               max_length=50)
