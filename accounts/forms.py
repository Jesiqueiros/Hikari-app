from django import forms


class LoginForm(forms.Form):

    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "class": "input",
            "placeholder": "correo@ejemplo.com",
            "autocomplete": "email"
        })
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "input",
            "placeholder": "••••••••",
            "autocomplete": "current-password"
        })
    )