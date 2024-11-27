from django import forms
# Form for adding/editing products
class NewDataForm(forms.Form):
    def for_edit_product(self,prod_desc ,pric, quant, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['prod_description'].initial = prod_desc
        self.fields['prod_sale_price'].initial = pric
        self.fields['prod_quantity'].initial = quant

    prod_description = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'id_name',
            'placeholder': 'Enter product Description',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;height:100px'
        })
    )
    prod_sale_price = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter product price',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
        })
    )

    prod_quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter product quantity',
            'class': 'form-control',
            'style': 'width: 100%; padding: 10px; margin-bottom: 10px;'
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