from django import forms
from django.core.validators import RegexValidator, MinValueValidator,MaxLengthValidator,MinLengthValidator

class returnProduct(forms.Form):
    def for_edit_return_product(self, prod_code, quantity, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prod_code'].initial = prod_code
        self.fields['quantity'].initial = quantity

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
class return_product_recipt_code(forms.Form):
    recipt_code_buy = forms.CharField(
        required=False,  # Make it not required because it will only be asked once
        max_length=6,  # Ensure the total length is 7
        min_length=6,
        widget=forms.TextInput(attrs={
            'placeholder': 'Receipt Code',
            'class': 'form_product-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;',
        }),
        validators=[
            RegexValidator(
                regex=r'^_[A-Za-z0-9]{5}$',
                message="Receipt code must start with '_' and be followed by 6 alphanumeric characters."
            )
        ]
    )

    def for_edit_recipt_code(self, recipt_code_buy, *args, **kwargs):
        """Set the receipt code if it's being edited or provided in the session."""
        super().__init__(*args, **kwargs)
        self.fields['recipt_code_buy'].initial = recipt_code_buy
