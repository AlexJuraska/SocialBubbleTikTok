/**
 * Saves the links of videos in a user page into a .txt file
 */
function saveVideosToFile() {
    const elements = document.querySelectorAll('a.css-1mdo0pl-AVideoContainer.e19c29qe4');

    const uniqueHrefs = new Set();

    elements.forEach(element => {
        const href = element.getAttribute('href');

        if (href && href.trim() !== "") {
            uniqueHrefs.add(href.trim());
        }
    });

    const filteredHrefs = Array.from(uniqueHrefs);

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

        console.log("Video links saved");
    } else {
        console.log("Something went wrong");
    }
}

/*
javascript:(function(){
    function saveVideosToFile() {
        const elements = document.querySelectorAll('a.css-1mdo0pl-AVideoContainer.e19c29qe4');
        const uniqueHrefs = new Set();
        elements.forEach(element => {
        const href = element.getAttribute('href');
        if (href && href.trim() !== "") {
            uniqueHrefs.add(href.trim());
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

    saveVideosToFile();
})();
 */