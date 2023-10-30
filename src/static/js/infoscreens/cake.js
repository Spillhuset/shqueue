document.addEventListener('DOMContentLoaded', () => {
  updateTimeCountdowns();
  setInterval(updateTimeCountdowns, 1000);
});

async function updateQueue(data) {
  // div
  document.getElementById("queue-name").innerHTML = data.name;

  // currently playing
  document.getElementById("currently-playing-list").innerHTML = data.currently_playing.map(person => `
    <div>
      <h3 class="text-8xl text-center font-bold">${person.name}</h3>
      ${person.paused ?
        `<p class="text-5xl text-center">Pauset</p>` :
        `<p class="text-5xl text-center time-countdown" data-time-left-seconds="${person.time_left_in_seconds - 1}">${person.time_left_in_seconds > 0 ? secondsToTimeLeft(person.time_left_in_seconds) : "Spiller på overtid"}</p>`
      }
    </div>
  `).join("")

  // queued
  document.getElementById("queued-list").innerHTML = data.queued.map((person, index) => `
    <tr>
      <td class="text-6xl">${index + 1}.</td>
      <td class="text-6xl truncate max-w-xs">${person.name}</td>
      <td class="text-6xl text-right whitespace-nowrap">${person.eta_to_play_in_seconds > 0 ? `${Math.ceil(person.eta_to_play_in_seconds / 60)} min` : "Nå"}</td>
    </tr>
  `).join("")

  // avg wait time
  document.getElementById("avg-wait-time").dataset.avgWaitTimeSeconds = String(data.avg_wait_time_seconds);

  // paused
  const status = document.getElementById("status");
  if (data.active) status.innerText = "";
  else status.innerText = "Inaktiv";
}

function updateTimeCountdowns() {
  const elements = Array.from(document.getElementsByClassName('time-countdown'));
  elements.forEach(element => {
    const timeLeftSeconds = parseInt(element.dataset.timeLeftSeconds);
    element.dataset.timeLeftSeconds -= 1;

    if (timeLeftSeconds > 0) element.innerHTML = secondsToTimeLeft(timeLeftSeconds);
    else element.innerHTML = `Spiller på overtid`;
  })

  const element = document.getElementById("avg-wait-time");
  const avgWaitTimeSeconds = parseInt(element.dataset.avgWaitTimeSeconds);
  element.dataset.avgWaitTimeSeconds -= 1;

  if (avgWaitTimeSeconds > 60) element.innerHTML = secondsToTimeLeft(avgWaitTimeSeconds, false);
  else element.innerHTML = `Under et minutt`;
}

function secondsToTimeLeft(seconds, includeSeconds = true) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor(seconds / 60) % 60;
  const remainingSeconds = seconds % 60;
  return [
    hours && `${hours} time${hours == 1 ? "" : "r"}`,
    minutes && `${minutes} min`,
    includeSeconds && remainingSeconds && `${remainingSeconds} sek`
  ].filter(Boolean).join(", ")
}
