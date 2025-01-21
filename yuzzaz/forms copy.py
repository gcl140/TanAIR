from django import forms
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    # Ensure email is used as the username
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'phone_number', 'email',  # Use email as username
            'company', 'address', 'profile_picture', 'bank_account_number',
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = self.cleaned_data["email"]  # Set the username to email
        if commit:
            user.save()
        return user
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'company', 'address', 'profile_picture', 'bank_account_number']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: Apply some style or widget changes, like custom fields or form layouts