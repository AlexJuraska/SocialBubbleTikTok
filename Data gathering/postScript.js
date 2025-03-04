/**
 * Saves the usernames of commenters below the video into a .txt file
 */
function savePostToFile() {

  const uniqueTagHrefs = new Set();

  // Getting hashtags
  const hashtagElements = document.querySelectorAll('strong');
  hashtagElements.forEach(hashtag => {
    const text = hashtag.textContent

    if (text.trim() && text.includes('#') && text.trim().replace(/#/g, '') !== "") {
      uniqueTagHrefs.add(text.trim());
    }
  });

  // Getting comments
  const elements = document.querySelectorAll('a.link-a11y-focus');
  const uniqueUserHrefs = new Set();

  elements.forEach(element => {
    let href = element.getAttribute('href');

    // Filtering hrefs beginning with "/@"
    if (href.trim() && href.trim().startsWith('/@')) {
      href = href.trim().substring(1);
      if (href.trim().replace(/@/g, '') !== "") {
        uniqueUserHrefs.add(href); // Remove the '/' at the start
      }
    }
  });

  const filteredTagHrefs = Array.from(uniqueTagHrefs);
  const filteredUserHrefs = Array.from(uniqueUserHrefs);

  if (filteredTagHrefs.length > 0 || filteredUserHrefs.length > 0) {

    const hrefsToSave = filteredTagHrefs.join('\n') + '\n\n' + filteredUserHrefs.join('\n');

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


// javascript:(function(){
//   function savePostToFile() {
//     const uniqueTagHrefs = new Set();
//     const hashtagElements = document.querySelectorAll('strong');
//     hashtagElements.forEach(hashtag => {
//       const text = hashtag.textContent;
//       if (text.trim() && text.includes('#') && text.trim().replace(/#/g, '') !== "") {uniqueTagHrefs.add(text.trim());}
//     });
//     const elements = document.querySelectorAll('a.link-a11y-focus');
//     const uniqueUserHrefs = new Set();
//     elements.forEach(element => {
//       let href = element.getAttribute('href');
//       if (href.trim() && href.trim().startsWith('/@')) {
//         href = href.trim().substring(1);
//         if (href.trim().replace(/@/g, '') !== "") {uniqueUserHrefs.add(href);}
//       }
//     });
//     const filteredTagHrefs = Array.from(uniqueTagHrefs);
//     const filteredUserHrefs = Array.from(uniqueUserHrefs);
//     if (filteredTagHrefs.length > 0 || filteredUserHrefs.length > 0) {
//       const hrefsToSave = filteredTagHrefs.join('\n') + '\n\n' + filteredUserHrefs.join('\n');
//       const blob = new Blob([hrefsToSave], { type: 'text/plain' });
//       const link = document.createElement('a');
//       link.href = URL.createObjectURL(blob);
//       link.download = window.location.href.replace(/^https:\/\/www\.tiktok\.com\//, '').replace(/\//g, '-') + '.txt';
//       link.click();
//     }
//   }
//   savePostToFile()
// })();
