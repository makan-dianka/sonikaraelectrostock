from django import forms

from .models import Payment


class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        self.sale = kwargs.pop('sale', None)
        self.purchase = kwargs.pop('purchase', None)

        super().__init__(*args, **kwargs)

        # pre-remplir le champ montant
        if self.sale:

            remaining = self.sale.remaining_amount

            if remaining and remaining > 0:
                self.fields['amount'].initial = remaining
            else:
                self.fields['amount'].initial = self.sale.total


        elif self.purchase:

            remaining = self.purchase.remaining_amount

            if remaining and remaining > 0:
                self.fields['amount'].initial = remaining
            else:
                self.fields['amount'].initial = self.purchase.total



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