from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

def index(request):
  if not request.user.is_authenticated:
    if settings.SHAUTH_SYSTEM_NAME is None: return redirect("/accounts/login")
    else: return redirect("/auth")
  return render(request, "shqueue/index.html")

@login_required
def view_queue(request, queue_id):
  queue = GameQueue.objects.get(id=queue_id)
  return render(request, "shqueue/view_queue.html", {"queue": queue})

@login_required
def add_to_queue(request, queue_id):
  queue = GameQueue.objects.get(id=queue_id)
  if request.method == "POST":
    form = AddPersonToQueueForm(request.POST)
    if form.is_valid():
      person = form.save(commit=False)
      person.queue = queue
      person.queue_position = QueuedPerson.objects.filter(queue=queue).order_by('-queue_position').first().queue_position + 1 if QueuedPerson.objects.filter(queue=queue).count() > 0 else 1
      person.finishing_at = timezone.now() + timezone.timedelta(seconds=queue.seconds_per_turn)
      person.queued_by = request.user
      person.save()
      return redirect(f'/queues/{queue_id}')
    return render(request, "errors/400.html", status=400)
  form = AddPersonToQueueForm()
  return render(request, "shqueue/add_to_queue.html", {"queue": queue, "form": form})

@login_required
def toggle_queue(request, queue_id):
  queue = GameQueue.objects.get(id=queue_id)
  queue.active = not queue.active
  queue.save()
  return redirect(f'/queues/{queue_id}')

@login_required
def clear_queue(request, queue_id):
  queue = GameQueue.objects.get(id=queue_id)
  queue.queued.all().delete()
  return redirect(f'/queues/{queue_id}')

@login_required
def remove_from_queue(request, queue_id, person_id):
  queue = GameQueue.objects.get(id=queue_id)
  person = QueuedPerson.objects.get(id=person_id)
  if person.queue == queue:
    person.delete()
    return redirect(f'/queues/{queue_id}')
  return render(request, "errors/400.html", status=400)

@login_required
def start_queued_person(request, queue_id, person_id):
  queue = GameQueue.objects.get(id=queue_id)
  person = QueuedPerson.objects.get(id=person_id)
  if person.queue == queue and person.playing_at is None:
    person.playing_at = timezone.now()
    person.finishing_at = timezone.now() + timezone.timedelta(seconds=queue.seconds_per_turn)
    person.save()
    return redirect(f'/queues/{queue_id}')
  return render(request, "errors/400.html", status=400)

@login_required
def pause_queued_person(request, queue_id, person_id):
  queue = GameQueue.objects.get(id=queue_id)
  person = QueuedPerson.objects.get(id=person_id)
  if person.queue == queue and person.playing_at is not None:
    if person.paused_at is None:
      person.paused_at = timezone.now()
    else:
      person.finishing_at += timezone.now() - person.paused_at
      person.paused_at = None
    person.save()
    return redirect(f'/queues/{queue_id}')
  return render(request, "errors/400.html", status=400)

@login_required
def finish_queued_person(request, queue_id, person_id):
  queue = GameQueue.objects.get(id=queue_id)
  person = QueuedPerson.objects.get(id=person_id)
  if person.queue == queue and person.playing_at is not None:
    person.stopped_at = timezone.now()
    person.save()
    return redirect(f'/queues/{queue_id}')
  return render(request, "errors/400.html", status=400)

@login_required
def move_queued_person(request, queue_id, person_id, move):
  queue = GameQueue.objects.get(id=queue_id)
  person = QueuedPerson.objects.get(id=person_id)
  if person.queue == queue:
    if move == "up":
      if person.queue_position_fixed > 1:
        other_person = queue.queued.order_by('-queue_position').filter(queue_position__lt=person.queue_position).first()
        other_person.queue_position = person.queue_position
        other_person.save()
        person.queue_position -= 1
        person.save()
    elif move == "down":
      if person.queue_position_fixed < person.queue.queued.count():
        other_person = queue.queued.order_by('queue_position').filter(queue_position__gt=person.queue_position).first()
        other_person.queue_position = person.queue_position
        other_person.save()
        person.queue_position += 1
        person.save()
    return redirect(f'/queues/{queue_id}')
  return render(request, "errors/400.html", status=400)
