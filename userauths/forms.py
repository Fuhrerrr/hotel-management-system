from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ImageField, FileInput, TextInput, Select
from userauths.models import Profile, User



class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': '', 'id': "", 'placeholder':'Full Name'}), max_length=100, required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': '', 'id': "", 'placeholder':'Username'}), max_length=100, required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': '' , 'id': "", 'placeholder':'Email Address'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'id': "", 'placeholder':'Password'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'id': "", 'placeholder':'Confirm Password'}), required=True)

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password1', 'password2']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'with-border'
            # visible.field.widget.attrs['placeholder'] = visible.field.label


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = [
            'image',
            'full_name', 
            'phone',
            'gender',
            'country',
            'city',
            'state',
            'address',
            'identity_type',
            'identity_image',
            'facebook',
            'twitter',
        ]
        widgets = {
            'image': FileInput(attrs={'onchange': 'loadFile(event)', 'class':'upload'}),
        }