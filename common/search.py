from .search_config import SEARCH_CONFIG
from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_api(request, entity):
    query = request.GET.get("q", "").strip()
    if query == "":
        return Response({"results": []})

    config = SEARCH_CONFIG.get(entity)
    if not config:
        return Response({"results": []}, status=404)

    q = Q()
    for field in config["search_fields"]:
        q |= Q(**{f"{field}__icontains": query})

    queryset = (
        config["queryset"]
        .filter(q)
        .order_by(config["order_by"])[:20]
    )

    serializer = config["serializer"](queryset, many=True)

    return Response({"results": serializer.data})