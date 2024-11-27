from django import forms
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
    # Form for adding/editing products
class ProductForm(forms.Form):
    def for_edit_product(self, code, quant, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prod_code'].initial = code
        self.fields['quantity'].initial = quant

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
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
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