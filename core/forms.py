from django import forms
from django.contrib.auth import get_user_model

from .models import Review, Ticket, UserFollow

User = get_user_model()


class TicketForm(forms.ModelForm):
    # edit_Ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    title = forms.CharField(
        widget=forms.widgets.TextInput(attrs={"placeholder": "Titre", "size": 100})
    )

    description = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={"placeholder": "Votre texte", "cols": "100"}
        )
    )

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    # edit_Review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    headline = forms.CharField(
        widget=forms.widgets.TextInput(attrs={"placeholder": "Titre"})
    )

    body = forms.CharField(
        widget=forms.widgets.Textarea(
            attrs={"placeholder": "Votre critique", "cols": "100"}
        )
    )

    rating = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect(attrs={"class": "rate"}),
        initial=3,
        choices=[(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
    )

    class Meta:
        model = Review
        fields = ["rating", "headline", "body"]


class UsersFollowForm(forms.ModelForm):
    class Meta:
        model = UserFollow
        fields = ["followed_user"]

    # def __init__(self, *args, **kwargs):
    #     qs = kwargs.pop('qs')
    #     super().__init__(*args, **kwargs)
    #     self.fields['followed_user'].queryset = qs


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
