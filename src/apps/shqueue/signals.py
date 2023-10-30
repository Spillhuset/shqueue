from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

from .models import *


def send_infoscreen_data(queue_id):
  channel_layer = get_channel_layer()
  queue = GameQueue.objects.get(id=queue_id)
  async_to_sync(channel_layer.group_send)(f'infoscreen_{queue_id}', {
    "type": "send_data",
    "data": json.dumps({
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
    })
  })
  print("done")

@receiver(post_save, sender=GameQueue)
def post_save_gamequeue(sender, instance, **kwargs): send_infoscreen_data(instance.id)

@receiver(post_save, sender=QueuedPerson)
def post_save_queuedperson(sender, instance, **kwargs): send_infoscreen_data(instance.queue.id)

@receiver(post_delete, sender=QueuedPerson)
def post_delete_queuedperson(sender, instance, **kwargs): send_infoscreen_data(instance.queue.id)
