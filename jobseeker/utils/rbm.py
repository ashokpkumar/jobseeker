from django import forms



class CreateUserForm(forms.Form):  # creation of signup table format for the databse
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    password = forms.CharField(required=True)

class FillNewUserForm(forms.Form):
    firstname = forms.CharField(required=True)
    lastname = forms.CharField()
    gender = forms.CharField(required=True)
    nationality = forms.CharField(required=True)
    country_code = forms.IntegerField(required=True)
    user_type = forms.CharField(required=True)

class LookUpTableForm(forms.Form):
    master_key = forms.CharField(required=True)
    key = forms.CharField(required=True)
    value = forms.IntegerField(required=True)

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

rbm_map = {
    'create_user':CreateUserForm,
    'fill_newuser':FillNewUserForm,
    'lookup':LookUpTableForm,
    'login':LoginForm
}

