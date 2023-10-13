document.addEventListener('DOMContentLoaded', () => {
  updateQueue(true);
  setInterval(updateQueue, 10000);

  updateTimeCountdowns();
  setInterval(updateTimeCountdowns, 1000);
});

async function updateQueue(init = false) {
  const data = await fetch("data").then(res => res.json());
  console.log(data);

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
  const avgWaitTimeHours = Math.floor(data.avg_wait_time_seconds / 3600);
  const avgWaitTimeMinutes = Math.floor(data.avg_wait_time_seconds / 60) % 60;
  document.getElementById('avg-wait-time').innerHTML = [
    avgWaitTimeHours && `${avgWaitTimeHours} timer`,
    avgWaitTimeMinutes && `${avgWaitTimeMinutes} minutter`
  ].filter(Boolean).join(", ") || "Under et minutt"
}

function updateTimeCountdowns() {
  const elements = Array.from(document.getElementsByClassName('time-countdown'));
  elements.forEach(element => {
    const timeLeftSeconds = parseInt(element.dataset.timeLeftSeconds);
    element.dataset.timeLeftSeconds -= 1;

    if (timeLeftSeconds > 0) element.innerHTML = secondsToTimeLeft(timeLeftSeconds);
    else element.innerHTML = `Spiller på overtid`;
  })
}

function secondsToTimeLeft(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return [
    minutes && `${minutes} min`,
    `${remainingSeconds} sek`
  ].filter(Boolean).join(", ")
}
