from django.urls import path

from api import views
from api.controllers import country, customer, film

urlpatterns = [
    path("", views.home, name="home"),
    path("countries", country.get_counties, name="api.countries"),
    path("datatable/customers", customer.datatable_search,
         name="api.datatable.customers"),
    path("datatable/films", film.datatable_search,
         name="api.datatable.customers"),
]
