import json
import os

# TODO Kinda forgot to actually add the comments themselves so yeah

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
                data[user]["commentsPosted"].append(
                    {
                        "text": text,
                        "likes": likes,
                        "hashtags": list(hashtags),
                    }
                )
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

            #TODO Test

    def __getDataFromFile(self, filename: str) -> (set[str], set[tuple[str, str, int]]):
        """
        Function reads the provided file and discerns the hashtags and usernames/comments/likes from it

        Source file should be .txt with format hashtags each in a new line. There should be
        an empty line separating the two sections. The other section should be "@user$Comment$likes".

        :param filename: name of the source file
        :return: Sets containing hashtags and tuples containing the rest of the data respectively
        """
        with open(filename, "r", encoding="UTF-8") as f:
            data = f.read().strip().split("\n\n")

            hashtags = set(data[0].split("\n"))

            comments = set()

            commentsLines = data[1].split("\n")
            for line in commentsLines:
                sep = line.split("$")
                comments.add((sep[0], sep[1], int(sep[2])))

            return hashtags, comments

    def __storeHashtagStatistics(self, hashtags: set[str]) -> None:
        """
        Function to store the number of hashtag appearances in self.hashtagFile
        :param hashtags: set of strings in format # + text
        :return: None
        """

        with open(self.hashtagFile, "r") as file:
            data = json.load(file)

        for tag in hashtags:
            if tag in data.keys():
                data[tag][0] += 1
            else:
                data[tag] = [ 1 ]

        with open(self.hashtagFile, "w") as file:
            json.dump(data, file, indent=3)

if __name__ == "__main__":
    p = DataParser("../Data/Information/testData.json", "../Data/Information/testHashtags.json")
    p.parseDirectoryCommentsData("../Data/Comments")