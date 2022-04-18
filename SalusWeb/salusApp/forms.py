from django import forms
from .models import Person, User
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'password', 'password2')
    
    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password is not None and password != password2:
            self.add_error("password2", "Your passwords must match")
        return cleaned_data

    def save(self,commit = True):   
        cleaned_data = self.clean()
        user = super(UserCreateForm, self).save(commit = False)
        user.username = self.cleaned_data['username']
        user.password = self.cleaned_data['password']
        if commit:
            user.save()
        return user
    
    
class PersonCreateForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'age', 'photo', 'address', 'sex', 'phone', 'idNumber', 'isDoctor', 'isNurse')
        

class PersonUpdateForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'age', 'photo', 'address', 'sex', 'phone', 'idNumber', 'isDoctor', 'isNurse')