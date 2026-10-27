import unicodedata
from datetime import date
from django import forms
from members.report_engine import VALUES, current_age
from .models import DatingProfile


def valid_name(value):
    value = unicodedata.normalize("NFC", " ".join(value.split()))
    letters = [char for char in value.upper() if char.isalpha()]
    if not letters or any(char not in VALUES for char in letters):
        raise forms.ValidationError("name_alphabet")
    if any(not char.isalpha() and char not in " -'’" for char in value):
        raise forms.ValidationError("name_alphabet")
    return value


def adult_date(value):
    age = current_age(value.isoformat(), date.today())
    if value > date.today() or not 18 <= age <= 120:
        raise forms.ValidationError("adult_only")
    return value


class PersonForm(forms.Form):
    full_name = forms.CharField(max_length=120)
    birth_date = forms.DateField(widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
    def clean_full_name(self):
        return valid_name(self.cleaned_data["full_name"])

    def clean_birth_date(self):
        return adult_date(self.cleaned_data["birth_date"])


class ProfileForm(forms.ModelForm):
    consent = forms.BooleanField(required=True)
    class Meta:
        model = DatingProfile
        fields = ["full_name", "birth_date", "alias", "city", "gender", "seeking",
                  "intent", "min_age", "max_age", "is_visible"]
        widgets = {"birth_date": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
                   "min_age": forms.NumberInput(attrs={"min": 18, "max": 120}),
                   "max_age": forms.NumberInput(attrs={"min": 18, "max": 120})}

    clean_full_name = lambda self: valid_name(self.cleaned_data["full_name"])
    clean_birth_date = lambda self: adult_date(self.cleaned_data["birth_date"])

    def clean(self):
        data = super().clean()
        minimum, maximum = data.get("min_age"), data.get("max_age")
        if minimum is not None and maximum is not None:
            if not 18 <= minimum <= maximum <= 120:
                self.add_error("min_age", "age_range")
        return data
