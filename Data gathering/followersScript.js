/**
 * Saves the usernames of followers/following into a .txt file
 */
function saveFollowsToFile(name) {

    const countElement = document.querySelector('strong[title=' + name + ']');
    const nameCount = countElement.innerText;

    const followsLiWrapper = document.querySelectorAll("li")
    const uniqueFollowers = new Set();

    followsLiWrapper.forEach(followsDiv => {
        const followATag = followsDiv.querySelector("a.css-7fu252-StyledUserInfoLink.es616eb3.link-a11y-focus");
        const username = followATag.getAttribute("href").substring(1);

        uniqueFollowers.add(username);
    });

    const filteredFollows = Array.from(uniqueFollowers);

    var hrefsToSave = nameCount;

    if (filteredFollows.length > 0) {
        hrefsToSave += "\n" + filteredFollows.join("\n");
    }

    const blob = new Blob([hrefsToSave], { type: "text/plain" });

    const link = document.createElement('a');

    link.href = URL.createObjectURL(blob);

    link.download = window.location.href.replace(/^https:\/\/www\.tiktok\.com\//, "").replace(/\//g, '-') +  " (" + name + ").txt";

    link.click();

    console.log(name + " links saved");
}

(function() {
    document.addEventListener("keydown", function(event) {
        if (event.key.toLowerCase() === "z") {
            saveFollowsToFile("Following");
        } else if (event.key.toLowerCase() === "x") {
            saveFollowsToFile("Followers");
        }
    });
})();

