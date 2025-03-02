from django import forms
from django.core.validators import RegexValidator, MinValueValidator,MaxLengthValidator,MinLengthValidator

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

    
    # Form for adding/editing products
class ProductForm(forms.Form):
    def for_edit_product(self, code, quant, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prod_code'].initial = code
        self.fields['quantity'].initial = quant

    prod_code = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={
            'id': 'id_prod_code',
            'placeholder': 'Enter product code',
            'class': 'form_product-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    quantity = forms.IntegerField(
        validators=[
            MinValueValidator(1, message="Quantity must be greater than or equal to 1")
        ],
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter product quantity',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;',
            'min': '1'  # HTML5 'min' attribute
        })
    )

# Form for adding/editing customer details
class CustomerForm(forms.Form):
    def for_edit_customer(self, customer_name, customer_email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer_name'].initial = customer_name
        self.fields['customer_email'].initial = customer_email

    customer_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Customer name',
            'class': 'form_product-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;',
        })
    )
    customer_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Customer email',
            'class': 'form_product-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;',
        })
    )