from .models import GameQueue

def navigation_links(request):
  queues = GameQueue.objects.all()
  return {
    'sidebar_items': [
      { 'title': 'Hjem', 'url': '/' },
    ] + [{ 'title': str(queue), 'url': f'/queues/{queue.id}'} for queue in queues]
  }

def queue(request):
  queues = GameQueue.objects.all()
  return {'queues': queues}
