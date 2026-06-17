from django import forms

from .models import Document


class DocumentForm(
    forms.ModelForm
):

    class Meta:

        model = Document

        fields = [

            'document_type',

            'purchase',

            'sale'

        ]

        widgets = {

            'document_type': forms.Select(

                attrs={

                    'class':'form-control'

                }

            ),

            'purchase': forms.Select(

                attrs={

                    'class':'form-control'

                }

            ),

            'sale': forms.Select(

                attrs={

                    'class':'form-control'

                }

            ),

        }


    def clean(self):

        cleaned = (

            super()

            .clean()

        )

        doc_type = (

            cleaned

            .get(
                'document_type'
            )

        )

        purchase = (

            cleaned

            .get(
                'purchase'
            )

        )

        sale = (

            cleaned

            .get(
                'sale'
            )

        )


        if (

            doc_type

            ==

            'purchase_order'

            and

            not purchase

        ):

            raise forms.ValidationError(

                "Sélectionnez un achat."

            )


        if (

            doc_type

            in [

                'invoice',

                'delivery_note'

            ]

            and

            not sale

        ):

            raise forms.ValidationError(

                "Sélectionnez une vente."

            )


        return cleaned