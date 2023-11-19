from django import forms


class GroupForm(forms.Form):
    group = forms.CharField(label="Your group", max_length=10)

