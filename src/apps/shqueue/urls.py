from . import views
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
  path("", views.index, name="index"),
  path("queues/<int:queue_id>", views.view_queue, name="view_queue"),
  path("queues/<int:queue_id>/add", views.add_to_queue, name="add_queued_person"),
  path("queues/<int:queue_id>/toggle", views.toggle_queue, name="toggle_queue"),
  path("queues/<int:queue_id>/clear", views.clear_queue, name="clear_queue"),
  path("queues/<int:queue_id>/remove/<int:person_id>", views.remove_from_queue, name="remove_queued_person"),
  path("queues/<int:queue_id>/start/<int:person_id>", views.start_queued_person, name="start_queued_person"),
  path("queues/<int:queue_id>/pause/<int:person_id>", views.pause_queued_person, name="pause_queued_person"),
  path("queues/<int:queue_id>/finish/<int:person_id>", views.finish_queued_person, name="finish_queued_person"),
  path("queues/<int:queue_id>/move/<int:person_id>/<str:move>", views.move_queued_person, name="move_queued_person"),
]
