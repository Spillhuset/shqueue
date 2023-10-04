from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

import math

class GameQueue(models.Model):
  name = models.CharField(max_length=100)
  active = models.BooleanField(default=False)
  capacity = models.IntegerField(default=1)
  seconds_per_turn = models.IntegerField(default=900)

  def __str__(self): return f'{self.name} ({str(self.queued.count())} i kø, ventetid: {str(self.avg_wait_time_minutes)} min)' if self.active else f'{self.name} (inaktiv)'

  @property
  def queued(self): return QueuedPerson.objects.filter(queue=self, playing_at=None).order_by('queue_position')

  @property
  def currently_playing(self): return QueuedPerson.objects.filter(queue=self, stopped_at=None).exclude(playing_at=None).order_by('playing_at')

  @property
  def avg_wait_time_seconds(self): return math.ceil((self.seconds_per_turn * self.queued.count() / self.capacity) + min([person.time_left_in_seconds if person.time_left_in_seconds > 0 else 0 for person in self.currently_playing] or [0]))

  @property
  def avg_wait_time_minutes(self): return math.ceil(self.avg_wait_time_seconds / 60)


class QueuedPerson(models.Model):
  name = models.CharField(max_length=100)
  queue = models.ForeignKey(GameQueue, on_delete=models.CASCADE)
  queue_position = models.IntegerField()

  queued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="queued_by")
  started_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="started_by")

  queued_at = models.DateTimeField(default=timezone.now)
  playing_at = models.DateTimeField(blank=True, null=True)
  paused_at = models.DateTimeField(blank=True, null=True)
  finishing_at = models.DateTimeField(blank=True, null=True)
  stopped_at = models.DateTimeField(blank=True, null=True)

  def __str__(self): return f'{self.name} i {self.queue.name} ({self.status}, kønr: {self.queue_position})'

  @property
  def queue_position_fixed(self):
    return self.queue.queued.filter(queue_position__lt=self.queue_position).count() + 1

  @property
  def status(self):
    if self.stopped_at: return "Ferdig"
    if self.paused_at: return "Pauset"
    if self.finishing_at is not None and self.finishing_at < timezone.now(): return "Spiller på overtid"
    if self.playing_at: return "Spiller"
    return "Venter"

  @property
  def time_left_in_seconds(self):
    if self.finishing_at is None: return 0
    now = timezone.now()
    if self.finishing_at < now: return -(now - self.finishing_at).seconds
    if self.finishing_at > now: return (self.finishing_at - now).seconds
    return 0

  @property
  def time_left_in_minutes(self): return math.ceil(self.time_left_in_seconds / 60)

  @property
  def eta_to_play_in_seconds(self):
    if self.playing_at: return 0
    queued = self.queue.queued.filter(queue_position__lt=self.queue_position).count()
    playing = self.queue.currently_playing.filter(queue_position__lt=self.queue_position)
    return (queued * self.queue.seconds_per_turn + sum([person.time_left_in_seconds if person.time_left_in_seconds > 0 else 0 for person in playing] or [0])) / self.queue.capacity

  @property
  def eta_to_play_in_minutes(self): return math.ceil(self.eta_to_play_in_seconds / 60)
