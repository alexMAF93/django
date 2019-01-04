from django import forms


class SendJokeForm(forms.Form):
    send_to_email = forms.EmailField(required=True)


class SubscribeToJokesForm(forms.Form):
    subscribe_email = forms.EmailField(required=True)
