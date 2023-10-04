from . import views
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
  path("queues/<int:queue_id>/data", views.queue_data, name="queue_data"),
  path("queues/<int:queue_id>/<str:type>", views.show_infoscreen, name="show_infoscreen")
]
