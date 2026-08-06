import os

from django.utils import timezone


def company_logo_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    return f"companies/{instance.uuid}/logo.{ext}"


def get_company_logo_path(company):
    """
    Retourne le chemin filesystem absolu du logo de l'entreprise,
    ou celui du logo par défaut si absent.
    """
    if company and company.logo:
        try:
            if os.path.exists(company.logo.path):
                return company.logo.path
        except (ValueError, FileNotFoundError):
            pass  # fichier manquant ou champ vide malgré le check



def generate_reference(prefix, model, company=None):
    """
    Génère une référence unique.

    Exemple :
        ACH-202607-0001
        VEN-202607-0001
        DOC-202607-0001
        DEV-202607-0001
    """

    now = timezone.now()

    prefix = f"{prefix}-{now:%Y%m}"

    last_object = (
        model.objects
        .filter(reference__startswith=prefix)
        .order_by("-id")
        .first()
    )

    if last_object:
        last_number = int(last_object.reference.split("-")[-1])
        number = last_number + 1
    else:
        number = 1

    return f"{prefix}-{number:04d}"