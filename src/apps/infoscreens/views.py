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
