import json
import logging

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from ..models import Film

# Get an instance of a logger
logger = logging.getLogger("django")


@require_http_methods(["POST"])
def datatable_search(request):
    """ Search films from db """

    args = json.loads(
        request.body) if request.method == 'POST' and request.body else {}
    logger.debug("Input args: %s", args)

    data = Film.datatable_search(args)

    films = []
    for film in data['films']:
        film_dict = film.row2dict()
        film_dict['language'] = film.language.row2dict()
        film_dict['categories'] = [category.row2dict()
                                   for category in film.categories.all()]
        film_dict['actors'] = [actor.row2dict()
                               for actor in film.actors.all()]
        films.append(film_dict)

    response = {
        'fetch_id':  args.get('fetch_id'),
        'records_total': data['records_total'],
        'records_filtered': data['records_filtered'],
        'data': films,
    }

    return JsonResponse(response, json_dumps_params={'indent': 2})
