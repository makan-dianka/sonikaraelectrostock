from django.utils import timezone

def generate_reference(prefix, model):
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