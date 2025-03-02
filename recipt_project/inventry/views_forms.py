from django import forms
from django.core.validators import RegexValidator, MinValueValidator

# Form for adding/editing products
class NewDataForm(forms.Form):
    def for_edit_product(self,prod_desc ,pric, quant, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prod_description'].initial = prod_desc
        self.fields['prod_sale_price'].initial = pric
        self.fields['prod_quantity'].initial = quant

    prod_description  = forms.CharField(
        widget=forms.Textarea(attrs={
            'id': 'id_name',
            'placeholder': 'Enter Product discription',
            'class': 'form-control',
            'style': 'width: 95%; padding: 10px; margin-bottom: 10px; height: 100px;'
        })
    )
    prod_sale_price = forms.FloatField(
        validators=[
            MinValueValidator(0.0, message="Sale price must be greater than or equal to 0.0")
        ],
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter product price',
            'class': 'form-control',
            'style': 'width: 95%; padding: 10px; margin-bottom: 10px;',
            'min': '0.0',  # HTML5 'min' attribute
            'step': '0.01'  # Optional, specifies the step size for floats
        })
    )

    prod_quantity = forms.IntegerField(
        validators=[
            MinValueValidator(1, message="Quantity must be greater than or equal to 1")
        ],
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter product quantity',
            'class': 'form-control',
            'style': 'width: 95%; padding: 10px; margin-bottom: 10px;',
            'min': '1'  # HTML5 'min' attribute
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
