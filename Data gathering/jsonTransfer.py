import json
import os

class DataParser:
    def __init__(self, dataFile: str, hashtagFile: str):
        self.dataFile: str = dataFile
        self.hashtagFile: str = hashtagFile

    def parseFileCommentsData(self, source: str) -> None:
        """
        Function reads the source file and creates connections between the creator and commenters,
        as well as storing the associated hashtags as well as comment text and the number of likes.
        :param source: source filename
        :return: None
        """

        hashtags: set[str]
        comments: set[tuple[str, str, int]]
        hashtags, comments = self.__getDataFromFile(source)

        postCreator = source.split("/")[-1].split("-")[0]

        filteredComments = set()
        usernames = set()
        for entry in comments:
            user, text, likes = entry

            #NOTE possibly not needed if the scraping code is good enough
            if user == postCreator or user.startswith("@MS4"):  #EXPL @MS4 users are mentioned users, those we ignore
                continue

            usernames.add(user)
            filteredComments.add(entry)

        try:
            with open(self.dataFile, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}

        # Creator
        if postCreator in data.keys():
            data[postCreator]["connections"] = list( set(data[postCreator]["connections"]).union(usernames) )
            data[postCreator]["commenters"] = list( set(data[postCreator]["commenters"]).union(usernames) )
            data[postCreator]["hashtags"] = list( set(data[postCreator]["hashtags"]).union(hashtags) )
        else:
            data[postCreator] = {
                "connections": list(usernames),
                "commenters": list(usernames),
                "hashtags": list(hashtags),
                "commentsPosted": []
            }

        # All users except Creator
        for entry in filteredComments:
            user, text, likes = entry

            adjustedUsers = usernames.copy()
            adjustedUsers.remove(user)
            adjustedUsers.add(postCreator)
            if user in data.keys():
                data[user]["connections"] = list( set(data[user]["connections"]).union(adjustedUsers) )
                data[user]["hashtags"] = list( set(data[user]["hashtags"]).union(hashtags) )

                newComment = {
                    "text": text.strip().lower(),
                    "likes": likes,
                    "hashtags": sorted(list(hashtags))
                }

                if newComment not in [
                    {
                        "text": comment["text"].strip().lower(),
                        "likes": comment["likes"],
                        "hashtags": sorted(comment["hashtags"])
                    }
                    for comment in data[user]["commentsPosted"]
                ]:
                    data[user]["commentsPosted"].append(newComment)

            else:
                data[user] = {
                    "connections": list(adjustedUsers),
                    "commenters": [],
                    "hashtags": list(hashtags),
                    "commentsPosted": [
                        {
                            "text": text,
                            "likes": likes,
                            "hashtags": list(hashtags),
                        }
                    ],
                }

        with open(self.dataFile, "w") as file:
            json.dump(data, file, indent=3)

        self.__storeHashtagStatistics(hashtags)

    def parseDirectoryCommentsData(self, directory: str) -> None:
        """
        Function gets all the filenames from a directory and calls the parseCommentsData function.

        Important: the func ignores filenames starting with "--"

        :param directory: path to the directory from which the source files will be taken
        :return: None
        """

        try:
            files: list[str] = os.listdir(directory)
        except FileNotFoundError:
            print("Error: Directory not found.")
            return
        except PermissionError:
            print("Error: Permission denied.")
            return

        for file in files:
            if file.startswith("--") or not file.startswith("@") or not file.endswith(".txt"):
                continue

            self.parseFileCommentsData(f"{directory}/{file}")

    def __getDataFromFile(self, filename: str) -> (set[str], set[tuple[str, str, int]]):
        """
        Function reads the provided file and discerns the hashtags and usernames/comments/likes from it

        Source file should be .txt with format hashtags each in a new line. There should be
        an empty line separating the two sections. The other section should be "@user$Comment$likes".

        :param filename: name of the source file
        :return: Sets containing hashtags and tuples containing the rest of the data respectively
        """
        with open(filename, "r", encoding="UTF-8") as f:

            text = f.read()

            if text[:2] == "\n\n":
                hashtags = set()
                text = text[2:]
                commentsLines = text.split("\n")
            else:
                data = text.strip().split("\n\n")
                hashtags = set(data[0].split("\n"))
                commentsLines = data[1].split("\n")

            commentsLines = self.__cleanUpData(commentsLines)

            comments = set()

            for line in commentsLines:
                sep = line.split("$")

                likesMultiplier = 1
                if sep[2].count("K"):   # "55.8K" == 55800
                    likesMultiplier = 1000
                    sep[2] = sep[2].replace("K", "")

                comments.add((sep[0], sep[1], int(float(sep[2]) * likesMultiplier)))

            return hashtags, comments

    def __cleanUpData(self, lines: list[str]) -> list[str]:
        """
        Gets the comments data in form "@user$Comment$likes". It clears empty lines and
        connects up seperated comment lines
        :param lines: Data in form list["@user$Comment$likes"]
        :return: Cleaned data
        """

        retData = []

        for i, line in enumerate(lines):
            if line.strip() == "":
                continue

            if not line.startswith("@") and len(retData) > 0:
                retData[-1] = retData[-1] + " " + line
            else:
                retData.append(line)

        return retData

    def __storeHashtagStatistics(self, hashtags: set[str]) -> None:
        """
        Function to store the number of hashtag appearances in self.hashtagFile
        :param hashtags: set of strings in format # + text
        :return: None
        """

        try:
            with open(self.hashtagFile, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}

        for tag in hashtags:
            if tag in data.keys():
                data[tag]["count"] += 1
                data[tag]["connections"] = list(set(data[tag]["connections"]).union(hashtags))
                data[tag]["connections"].remove(tag)
            else:
                data[tag] = {"count": 1, "connections": list(hashtags)}
                data[tag]["connections"].remove(tag)

        with open(self.hashtagFile, "w") as file:
            json.dump(data, file, indent=3)

if __name__ == "__main__":
    p = DataParser("../Data/Information/data.json", "../Data/Information/hashtags.json")
    p.parseDirectoryCommentsData("../Data/Comments/")