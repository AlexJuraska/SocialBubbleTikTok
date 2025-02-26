/**
 * Scrolls for the selected duration and at the designated speed
 */
function scrollForDuration(duration, speed) {
  const startTime = Date.now();

  // Scroll every 100ms
  const interval = setInterval(() => {
    window.scrollBy(0, speed);

    if (Date.now() - startTime >= duration) {
      clearInterval(interval);
      console.log(`Scrolling stopped after ${duration}ms`);
    }
  }, 100); // The scroll called every 100ms
}

/*
javascript:(function(){
    function scrollForDuration(duration, speed) {
        const startTime = Date.now();

        const interval = setInterval(() => {
        window.scrollBy(0, speed);

        if (Date.now() - startTime >= duration) {
          clearInterval(interval);
        }
      }, 100);
    }

    scrollForDuration(15000,500);
})();
*/