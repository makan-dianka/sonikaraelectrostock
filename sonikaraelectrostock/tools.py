from django.utils import timezone


# Generation of reference number
def generate_reference(initial, obj):
    """Generation of reference number

    Args:
        initial (str): prefix of word
        obj (object): model object

    Returns:
        str: reference number
    """

    now = timezone.now()

    prefix = (
        f"{initial}-"
        f"{now:%Y%m}"
    )

    count = obj.objects.count() + 1

    return (

        f"{prefix}"

        f"-{count:04d}"
    )