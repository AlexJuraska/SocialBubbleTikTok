// #########################################
// # Script to be pasted into tampermonkey #
// #########################################

function parseShortNumber(str) {
    const num = parseFloat(str);
    if (str.toUpperCase().endsWith('K')) {
        return String(num * 1000);
    } else if (str.toUpperCase().endsWith('M')) {
        return String(num * 1000000);
    } else {
        return str;
    }
}

function scrollForDuration(duration, speed) {
  const startTime = Date.now();

  const interval = setInterval(() => {
    window.scrollBy(0, speed);

    if (Date.now() - startTime >= duration) {
      clearInterval(interval);
    }
  }, 100);
}

function savePostToFile() {

  const uniqueTagHrefs = new Set();
  const hashtagElements = document.querySelectorAll('strong');
  hashtagElements.forEach(hashtag => {
    const text = hashtag.textContent

    if (text.trim() && text.includes('#') && text.trim().replace(/#/g, "") !== "") {
      uniqueTagHrefs.add(text.trim());
    }
  });

  const countDivWrapper = document.querySelector("div.css-12ulmim-DivCommentCountContainer.ejcng164");
  const countSpan = countDivWrapper.querySelector("span.TUXText.TUXText--tiktok-sans.TUXText--weight-medium");
  const count = parseShortNumber(countSpan.textContent.split(" ")[0])

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

    const hrefsToSave = count + '\n' + filteredTagHrefs.join('\n') + '\n\n' + filteredComments.join('\n');

    const blob = new Blob([hrefsToSave], { type: "text/plain" });

    const link = document.createElement('a');

    link.href = URL.createObjectURL(blob);

    link.download = window.location.href.replace(/^https:\/\/www\.tiktok\.com\//, "").replace(/\//g, '-') + ".txt";

    link.click();
  }
}

function saveFollowsToFile(name) {

    if (!["Followers", "Following"].includes(name)) { return; }

    const countElement = document.querySelector('strong[title=' + name + ']');
    const nameCount = parseShortNumber(countElement.innerText);

    const followsLiWrapper = document.querySelectorAll("li")
    const uniqueFollowers = new Set();

    followsLiWrapper.forEach(followsDiv => {
        const followATag = followsDiv.querySelector("a.css-7fu252-StyledUserInfoLink.es616eb3.link-a11y-focus");
        const username = followATag.getAttribute("href").substring(1);

        uniqueFollowers.add(username);
    });

    const filteredFollows = Array.from(uniqueFollowers);
    let hrefsToSave = nameCount;

    if (filteredFollows.length > 0) {
        hrefsToSave += "\n" + filteredFollows.join("\n");
    }

    const blob = new Blob([hrefsToSave], { type: "text/plain" });

    const link = document.createElement('a');

    link.href = URL.createObjectURL(blob);

    link.download = window.location.href.replace(/^https:\/\/www\.tiktok\.com\//, "").replace(/\//g, '-') +  " (" + name + ").txt";

    link.click();
}

(function() {
    document.addEventListener("keydown", function(event) {
        if (event.code === "KeyZ") {
            saveFollowsToFile("Following");
        } else if (event.code === "KeyX") {
            saveFollowsToFile("Followers");
        } else if (event.code === "KeyC") {
            savePostToFile();
        } else if (event.code === "PageDown") {
            scrollForDuration(15000, 500);
        }
    });
})();
