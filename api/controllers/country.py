from django.http import JsonResponse

from ..models import Country


def get_counties(request):
    """ Get list of countries from db """
    countries = list(Country.objects.order_by('country').values())

    return JsonResponse(countries, safe=False, json_dumps_params={'indent': 2})
