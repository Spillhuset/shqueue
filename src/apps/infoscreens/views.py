from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt

from ..shqueue.models import *

@xframe_options_exempt
def show_infoscreen(request, queue_id, type):
  queue = GameQueue.objects.get(id=queue_id)
  preview = request.GET.get("preview", None) is not None
  try: return render(request, f"infoscreens/{type}.html", {"queue": queue, "preview": preview})
  except: return render(request, "errors/404.html", status=404)

def queue_data(request, queue_id):
  # django is stupid so we gotta send an array query apparently
  queue = GameQueue.objects.get(id=queue_id)
  return JsonResponse({
    "name": queue.name,
    "active": queue.active,
    "capacity": queue.capacity,
    "seconds_per_turn": queue.seconds_per_turn,
    "queued": [{
      "name": person.name,
      "eta_to_play_in_seconds": person.eta_to_play_in_seconds,
    } for person in queue.queued],
    "currently_playing": [{
      "name": person.name,
      "paused": person.paused_at is not None,
      "time_left_in_seconds": person.time_left_in_seconds,
    } for person in list(queue.currently_playing)],
    "avg_wait_time_seconds": queue.avg_wait_time_seconds,
  }, safe=False)
