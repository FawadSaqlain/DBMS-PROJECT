from django import forms
from django.core.validators import RegexValidator, EmailValidator

class NewDataForm(forms.Form):
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
        'oninput': "this.value = this.value.replace(/[^a-zA-Z]/g, '')",  # Only allow letters (no spaces or special characters)
        'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'id': 'id_last_name',
            'placeholder': 'Enter last name',
            'class': 'form-control',
            'oninput': "this.value = this.value.replace(/[^a-zA-Z]/g, '')",  # Only allow letters (no spaces or special characters)
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )

    cnic = forms.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\d{5}-\d{7}-\d{1}$',
                message="CNIC must be in the format 12345-1234567-1"
            )
        ],
        widget=forms.TextInput(attrs={
            'id': 'id_cnic',
            'placeholder': 'Enter CNIC (e.g., 12345-1234567-1)',
            'class': 'form-control',
            'oninput': "this.value = this.value.replace(/[^0-9-]/g, '')",  # Only allow digits and hyphens
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    phone_number = forms.CharField(
        max_length=13,
        validators=[
            RegexValidator(
                regex=r'^\+\d{12}$',
                message="Phone number must start with + and contain 12 digits (e.g., +92345678901)."
            )
        ],
        widget=forms.TextInput(attrs={
            'id': 'id_phone_number',
            'placeholder': 'Enter Phone Number (e.g., +92345678901)',
            'class': 'form-control',
            'oninput': "this.value = this.value.replace(/[^+0-9]/g, '')",  # Only allow + and digits
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    email = forms.EmailField(
        validators=[EmailValidator(message="Enter a valid email address.")],
        widget=forms.EmailInput(attrs={
            'id': 'id_email',
            'placeholder': 'Enter Email (e.g., example@domain.com)',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    username = forms.CharField(
    widget=forms.TextInput(attrs={
        'id': 'id_username',
        'placeholder': 'Enter username',
        'class': 'form-control',
        'oninput': "this.value = this.value.replace(/\\s/g, '')",  # Disallow spaces
        'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'id_password',
            'placeholder': 'Enter password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'  
        }),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_=+#%^()|}{;:/.>,<`~])[A-Za-z\d@$!%*?&_=+#%^()|}{;:/.>,<`~]{8,16}$',
                message="Password must be 8-16 characters long, include at least one uppercase letter, one lowercase letter, one number, and one special character."
            )
        ]
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'id_confirm_password',
            'placeholder': 'Enter confirm password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'  
        }),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_=+#%^()|}{;:/.>,<`~])[A-Za-z\d@$!%*?&_=+#%^()|}{;:/.>,<`~]{8,16}$',
                message="Password must be 8-16 characters long, include at least one uppercase letter, one lowercase letter, one number, and one special character."
            )
        ]
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
    def for_edit_user(self,first_name ,last_name, cnic,phone_number,email,user_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = first_name
        self.fields['last_name'].initial = last_name
        self.fields['cnic'].initial = cnic
        self.fields['phone_number'].initial = phone_number
        self.fields['email'].initial = email
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
        'oninput': "this.value = this.value.replace(/[^a-zA-Z]/g, '')",  # Only allow letters (no spaces or special characters)
        'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'id': 'id_last_name',
            'placeholder': 'Enter last name',
            'class': 'form-control',
            'oninput': "this.value = this.value.replace(/[^a-zA-Z]/g, '')",  # Only allow letters (no spaces or special characters)
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )

    cnic = forms.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\d{5}-\d{7}-\d{1}$',
                message="CNIC must be in the format 12345-1234567-1"
            )
        ],
        widget=forms.TextInput(attrs={
            'id': 'id_cnic',
            'placeholder': 'Enter CNIC 12345-1234567-1',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    phone_number = forms.CharField(
        max_length=13,
        validators=[
            RegexValidator(
                regex=r'^\+\d{12}$',
                message="Phone number must start with + and contain 12 digits (e.g., +92345678901)."
            )
        ],
        widget=forms.TextInput(attrs={
            'id': 'id_phone_number',
            'placeholder': 'Enter Phone Number (e.g., +92345678901)',
            'class': 'form-control',
            'oninput': "this.value = this.value.replace(/[^+0-9]/g, '')",  # Only allow + and digits
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
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'id': 'id_password',
            'placeholder': 'Enter password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'  
        }),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_=+#%^()|}{;:/.>,<`~])[A-Za-z\d@$!%*?&_=+#%^()|}{;:/.>,<`~]{8,16}$',
                message="Password must be 8-16 characters long, include at least one uppercase letter, one lowercase letter, one number, and one special character."
            )
        ]
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'id': 'id_confirm_password',
            'placeholder': 'Enter confirm password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        }),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_=+#%^()|}{;:/.>,<`~])[A-Za-z\d@$!%*?&_=+#%^()|}{;:/.>,<`~]{8,16}$',
                message="Password must be 8-16 characters long, include at least one uppercase letter, one lowercase letter, one number, and one special character."
            )
        ]
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

class ChangePasswordForm(forms.Form):
    password_validator = RegexValidator(
        regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_=+#%^()|}{;:/.>,<`~])[A-Za-z\d@$!%*?&_=+#%^()|}{;:/.>,<`~]{8,16}$',
        message="Password must be 8-16 characters long, include at least one uppercase letter, one lowercase letter, one number, and one special character."
    )

    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'id': 'id_old_password',
            'placeholder': 'Enter old password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        }),
        validators=[password_validator]
    )

    new_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'id': 'id_new_password',
            'placeholder': 'Enter new password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        }),
        validators=[password_validator]
    )

    confirm_new_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'id': 'id_confirm_new_password',
            'placeholder': 'Confirm new password',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        }),
        validators=[password_validator]
    )

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")
        return cleaned_data
