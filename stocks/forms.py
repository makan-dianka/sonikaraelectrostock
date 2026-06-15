from django import forms

class AddStockForm(forms.Form):

    quantity = forms.IntegerField(

        min_value=1,

        widget=forms.NumberInput(
            attrs={
                'class':'form-control',
                'placeholder':'Quantité'
            }
        )
    )