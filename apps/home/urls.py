
from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    # path(r'^.*\.*', views.pages),
    # path(r'^.*\.*', views.pages, name='pages'),
    # re_path(r'^.*\.*', views.pages, name='pages'),
]

# WARNINGS: path
# ?: (2_0.W001) Your URL pattern '^.*\.*' [name='pages'] has a route that contains '(?P<', begins with a '^', or ends with a '$'. This was likely an oversight when migrating to django.urls.path().
