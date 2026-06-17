from django import forms

from .models import Payment


class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.sale = kwargs.pop('sale', None)
        super().__init__(*args, **kwargs)

        # pré-remplissage du montant
        if self.sale:
            if self.sale.remaining_amount > 0:
                self.fields['amount'].initial = self.sale.remaining_amount
            else:
                self.fields['amount'].initial = self.sale.total



    class Meta:
        model = Payment

        exclude = [
            'sale',
            'created_by',
            'reference'
        ]

        widgets = {

            'amount': forms.NumberInput(

                attrs={

                    'class':'form-control'

                }

            ),

            'payment_method': forms.Select(

                attrs={

                    'class':'form-control'

                }

            ),

            'notes': forms.Textarea(

                attrs={

                    'class':'form-control'

                }

            )

        }