/**
 * Saves the usernames of commenters below the video into a .txt file
 */
function savePostToFile() {

  const uniqueTagHrefs = new Set();

  // Getting hashtags
  const hashtagElements = document.querySelectorAll('strong');
  hashtagElements.forEach(hashtag => {
    const text = hashtag.textContent

    if (text.trim() && text.includes('#') && text.trim().replace(/#/g, "") !== "") {
      uniqueTagHrefs.add(text.trim());
    }
  });

  // Getting comments
  const commentDivWrappers = document.querySelectorAll("div.e1970p9w2")
  const uniqueComments = new Set();

  commentDivWrappers.forEach(div => {
    const usernamePs = div.querySelectorAll('a.link-a11y-focus');
    const username = usernamePs[0].getAttribute("href").substring(1);

    const textPs = div.querySelectorAll("p.TUXText.TUXText--tiktok-sans.css-1658qcl-StyledTUXText.e1vx58lt0");
    const text = textPs[2].textContent;

    const likesPs = div.querySelectorAll("span.TUXText.TUXText--tiktok-sans.TUXText--weight-normal");
    const likes = likesPs[1].textContent;

    uniqueComments.add(`${username}$${text}$${likes}`);
  });

  const filteredTagHrefs = Array.from(uniqueTagHrefs);
  const filteredComments = Array.from(uniqueComments);

  if (filteredTagHrefs.length > 0 || filteredComments.length > 0) {

    const hrefsToSave = filteredTagHrefs.join('\n') + '\n\n' + filteredComments.join('\n');

    const blob = new Blob([hrefsToSave], { type: "text/plain" });

    const link = document.createElement('a');

    link.href = URL.createObjectURL(blob);

    link.download = window.location.href.replace(/^https:\/\/www\.tiktok\.com\//, "").replace(/\//g, '-') + ".txt";

    link.click();

    console.log("Usernames saved");
  } else {
    console.log("Something went wrong");
  }
}