/**
 * Scrolls for the selected duration and at the designated speed
 */
function scrollForDuration(duration, speed) {
  const startTime = Date.now();

  const interval = setInterval(() => {
    window.scrollBy(0, speed);

    if (Date.now() - startTime >= duration) {
      clearInterval(interval);
    }
  }, 100);
}