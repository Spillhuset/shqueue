function updateTimeCountdowns() {
  const elements = Array.from(document.getElementsByClassName('time-countdown'));
  elements.forEach(element => {
    const timeLeftSeconds = parseInt(element.dataset.timeLeftSeconds);
    element.dataset.timeLeftSeconds -= 1;
    if (timeLeftSeconds > 0) {
      element.innerHTML = secondsToTimeLeft(timeLeftSeconds);
    } else {
      if (timeLeftSeconds % 2) {
        element.parentElement.classList.add('bg-red-700');
      } else {
        element.parentElement.classList.remove('bg-red-700');
      }
      element.innerHTML = `Overtid med ${secondsToTimeLeft(-timeLeftSeconds)}`
    }
  });
}

document.addEventListener('DOMContentLoaded', updateTimeCountdowns);
setInterval(updateTimeCountdowns, 1000);

function secondsToTimeLeft(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes} min, ${remainingSeconds} sek`;
}
