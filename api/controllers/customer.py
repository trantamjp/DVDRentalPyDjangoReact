import json
import logging

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from ..models import Customer

# Get an instance of a logger
logger = logging.getLogger("django")


@require_http_methods(["POST"])
def datatable_search(request):
    """ Search customers from db """

    args = json.loads(
        request.body) if request.method == 'POST' and request.body else {}
    logger.debug("Input args: %s", args)

    data = Customer.datatable_search(args)

    customers = []
    for customer in data['customers']:
        cust_dict = customer.row2dict()
        cust_dict['address'] = customer.address.row2dict()
        cust_dict['address']['city'] = customer.address.city.row2dict()
        cust_dict['address']['city']['country'] = customer.address.city.country.row2dict()
        customers.append(cust_dict)

    response = {
        'fetch_id':  args.get('fetch_id'),
        'records_total': data['records_total'],
        'records_filtered': data['records_filtered'],
        'data': customers,
    }

    return JsonResponse(response, json_dumps_params={'indent': 2})
