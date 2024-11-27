from django import forms
class returnProduct(forms.Form):
    def for_edit_return_product(self, prod_code, quantity, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prod_code'].initial = prod_code
        self.fields['quantity'].initial = quantity

    prod_code = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'id_prod_code',
            'placeholder': 'Enter product code',
            'class': 'form_product-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter product quantity',
            'class': 'form_product-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;',
        })
    )
# Form for adding/editing customer details
class return_product_recipt_code(forms.Form):
    recipt_code_buy = forms.CharField(
        required=False,  # Make it not required because it will only be asked once
        widget=forms.TextInput(attrs={
            'placeholder': 'Receipt Code',
            'class': 'form_product-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;',
        })
    )

    def for_edit_recipt_code(self, recipt_code_buy, *args, **kwargs):
        """Set the receipt code if it's being edited or provided in the session."""
        super().__init__(*args, **kwargs)
        self.fields['recipt_code_buy'].initial = recipt_code_buy
