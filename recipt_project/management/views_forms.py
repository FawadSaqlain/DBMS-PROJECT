from django import forms

class NewDataForm(forms.Form):
    def for_edit_user(self,first_name ,last_name, cnic,phone_number,email,username,user_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = first_name
        self.fields['last_name'].initial = last_name
        self.fields['cnic'].initial = cnic
        # self.fields['password'].initial=password
        self.fields['phone_number'].initial = phone_number
        self.fields['email'].initial = email
        self.fields['username'].initial = username
        self.fields['user_type'].initial = user_type
    USER_TYPE_CHOICES = [
        ('inventory manager', 'Inventory Manager'),
        ('counter manager', 'Counter Manager'),
        ('administration manager', 'Administration Manager'),
    ]
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'id': 'id_first_name',
            'placeholder': 'Enter first name',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'id': 'id_last_name',
            'placeholder': 'Enter last name',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    cnic = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'id': 'id_cnic',
            'placeholder': 'Enter CNIC',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    phone_number = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={
            'id': 'id_phone_number',
            'placeholder': 'Enter Phone Number',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'id': 'id_email',
            'placeholder': 'Enter Email',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'id_username',
            'placeholder': 'Enter username',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'id_password',
            'placeholder': 'Enter password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'  
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'id_confirm_password',
            'placeholder': 'Enter confirm password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'  
        })
    )
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
            'style': 'margin-right: 10px; margin-bottom: 10px;'
        })
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'id': 'id_address',
            'placeholder': 'Enter Address',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px; height: 100px;'  
        })
    )
class NewDataForm_edit(forms.Form):
    def for_edit_user(self,first_name ,last_name, cnic,phone_number,email,username,user_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = first_name
        self.fields['last_name'].initial = last_name
        self.fields['cnic'].initial = cnic
        self.fields['phone_number'].initial = phone_number
        self.fields['email'].initial = email
        # self.fields['username'].initial = username
        self.fields['user_type'].initial = user_type
    USER_TYPE_CHOICES = [
        ('inventory manager', 'Inventory Manager'),
        ('counter manager', 'Counter Manager'),
        ('administration manager', 'Administration Manager'),
    ]
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'id': 'id_first_name',
            'placeholder': 'Enter first name',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'id': 'id_last_name',
            'placeholder': 'Enter last name',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    cnic = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'id': 'id_cnic',
            'placeholder': 'Enter CNIC',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'id': 'id_phone_number',
            'placeholder': 'Enter Phone Number',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'id': 'id_email',
            'placeholder': 'Enter Email',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    # username = forms.CharField(
    #     widget=forms.TextInput(attrs={
    #         'id': 'id_username',
    #         'placeholder': 'Enter username',
    #         'class': 'form-control',
    #         'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
    #     })
    # )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'id': 'id_password',
            'placeholder': 'Enter password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'  
        })
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'id': 'id_confirm_password',
            'placeholder': 'Enter confirm password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
            'style': 'margin-right: 10px; margin-bottom: 10px;'
        })
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'id': 'id_address',
            'placeholder': 'Enter Address',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px; height: 100px;'  
        })
    )
class changepassword(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'id_old_password',
            'placeholder': 'Enter old password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter new password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter confirm new password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )