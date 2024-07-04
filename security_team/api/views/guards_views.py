from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from security_team.api.serializers import AllSecurityGuardsSerializer
from security_team.models import SecurityGuard


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_guards_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_guards = SecurityGuard.objects.all().filter(user__is_archived=False)


    if search_query:
        all_guards = all_guards.filter(
            Q(user__email__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__department__icontains=search_query) |
            Q(user__gender__icontains=search_query) |
            Q(user__dob__icontains=search_query) |
            Q(user__marital_status__icontains=search_query) |
            Q(user__phone__icontains=search_query) |
            Q(user__country__icontains=search_query) |
            Q(user__language__icontains=search_query) |
            Q(user__location_name__icontains=search_query)
        )


    paginator = Paginator(all_guards, page_size)

    try:
        paginated_guards = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_guards = paginator.page(1)
    except EmptyPage:
        paginated_guards = paginator.page(paginator.num_pages)

    all_guards_serializer = AllSecurityGuardsSerializer(paginated_guards, many=True)


    data['guards'] = all_guards_serializer.data
    data['pagination'] = {
        'page_number': paginated_guards.number,
        'total_pages': paginator.num_pages,
        'next': paginated_guards.next_page_number() if paginated_guards.has_next() else None,
        'previous': paginated_guards.previous_page_number() if paginated_guards.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

