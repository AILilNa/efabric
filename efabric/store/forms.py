from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import Profile


class RegistrationForm(UserCreationForm):
    """
    Custom registration form with additional fields and improved styling.
    """

    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=1019,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=700,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        # Improved field styling and help text
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = ('<span class="form-text text-muted"><small>Choose a memorable username '
                                             '(less than 150 characters) using letters, numbers, and some symbols '
                                             '(e.g., username123, user_name).</small></span>')


class UpdateUserForm(UserChangeForm):
    # Hide Password stuff
    password = None
    # Get other fields
    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
                             required=False)
    first_name = forms.CharField(label="", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
                                 required=False)
    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
                                required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = ('<span class="form-text text-muted"><small>less than 150 characters using '
                                     'letters, numbers, and some symbols.</small></span>')


class UpdatePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['new_password1'].label = ''
        self.fields[
            'new_password1'].help_text = ('<ul class="form-text text-muted small"><li>Your password can\'t be too '
                                          'similar to your other personal information.</li><li>Your password must '
                                          'contain at least 8 characters.</li><li>Your password can\'t be a commonly '
                                          'used password.</li><li>Your password can\'t be entirely numeric.</li></ul>')

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['new_password2'].label = ''
        self.fields[
            'new_password2'].help_text = ('<span class="form-text text-muted"><small>Re-enter your '
                                          'password.</small></span>')


class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
                            required=False)
    address = forms.CharField(label="",
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address '}),
                              required=False)
    city = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
                           required=False)
    zipcode = forms.CharField(label="",
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}),
                              required=False)
    country = forms.CharField(label="",
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
                              required=False)

    class Meta:
        model = Profile
        fields = ('phone', 'address', 'city', 'zipcode', 'country',)
