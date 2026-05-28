from django import forms


class AvailabilitySearchForm(forms.Form):
    check_in_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    check_out_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    def clean_check_in_date(self):
        from django.utils import timezone

        cin = self.cleaned_data.get("check_in_date")
        if cin is None:
            return cin
        today = timezone.localdate()
        if cin < today:
            raise forms.ValidationError(
                "Past dates are not allowed. Please select today or a future date."
            )
        return cin

    def clean(self):
        cleaned = super().clean()
        cin = cleaned.get("check_in_date")
        cout = cleaned.get("check_out_date")
        if cin and cout:
            if cout <= cin:
                raise forms.ValidationError("Check-out date must be after check-in date.")
        return cleaned


class ReservationDetailsForm(forms.Form):
    adults = forms.IntegerField(min_value=1, initial=1)
    kids = forms.IntegerField(min_value=0, initial=0)
    seniors = forms.IntegerField(min_value=0, initial=0)

    def clean(self):
        cleaned = super().clean()
        adults = cleaned.get("adults") or 0
        kids = cleaned.get("kids") or 0
        seniors = cleaned.get("seniors") or 0
        if adults + kids + seniors <= 0:
            raise forms.ValidationError("At least 1 guest is required.")
        return cleaned
