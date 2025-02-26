/**
 * Saves the usernames of commenters below the video into a .txt file
 */
function saveCommentsToFile() {
  // Select all <a> username elements
  const elements = document.querySelectorAll('a.link-a11y-focus');

  const uniqueHrefs = new Set();

  elements.forEach(element => {
    const href = element.getAttribute('href');

    // Filtering hrefs beginning with "/@"
    if (href && href.trim().startsWith('/@')) {
      uniqueHrefs.add(href.trim().substring(1)); // Remove the '/' at the start
    }
  });

  const filteredHrefs = Array.from(uniqueHrefs);
  console.log(uniqueHrefs);

  if (filteredHrefs.length > 0) {

    const hrefsToSave = filteredHrefs.join('\n');

    const blob = new Blob([hrefsToSave], { type: 'text/plain' });

    // Create a link element to trigger the download
    const link = document.createElement('a');

    // Link to download the file
    link.href = URL.createObjectURL(blob);

    link.download = window.location.href.replace(/^https:\/\/www\.tiktok\.com\//, '').replace(/\//g, '-') + '.txt';

    // Click the download button
    link.click();

    console.log("Usernames saved");
  } else {
    console.log("Something went wrong");
  }
}

/*
javascript:(function(){
    function saveCommentsToFile() {
        const elements = document.querySelectorAll('a.link-a11y-focus');
        const uniqueHrefs = new Set();
        elements.forEach(element => {
        const href = element.getAttribute('href');
        if (href && href.trim().startsWith('/@')) {
            uniqueHrefs.add(href.trim().substring(1));
        }
        });
        const filteredHrefs = Array.from(uniqueHrefs);
        if (filteredHrefs.length > 0) {
            const hrefsToSave = filteredHrefs.join('\n');
            const blob = new Blob([hrefsToSave], { type: 'text/plain' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = window.location.href.replace(/^https:\/\/www\.tiktok\.com\//, '').replace(/\//g, '-') + '.txt';
            link.click();
        }
    }

    saveHrefsToFile();
})();
 */