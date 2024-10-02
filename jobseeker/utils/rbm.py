from django import forms



class CreateUserForm(forms.Form):  # creation of signup table format for the databse
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    password = forms.CharField(required=True)



rbm_map = {
    'create_user':CreateUserForm
}