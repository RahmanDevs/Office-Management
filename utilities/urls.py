from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.dev_urls, name='dev_urls'),
    # image resizer
    path('image-resizer/', TemplateView.as_view(template_name='utilitie/image_resizer.html'), name='image_resizer'),
    # Number to words converter
    path('number-to-words/', TemplateView.as_view(template_name='utilitie/number_to_word.html'), name='number_to_word'),
    

]

