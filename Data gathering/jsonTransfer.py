import json

# TODO Kinda forgot to actually add the comments themselves so yeah
# TODO Probably will need to change mostly the json design, __getDataFromFile

class DataParser:
    def __init__(self, dataFile: str, hashtagFile: str):
        self.dataFile: str = dataFile
        self.hashtagFile: str = hashtagFile

    def parseCommentsData(self, source: str) -> None:
        """
        Function reads the source file and creates connections between the creator and commenters,
        as well as storing the associated hashtags.
        :param source: source filename
        :return: None
        """
        hashtags, usernames = self.__getDataFromFile(source)

        postCreator = source.split("/")[-1].split("-")[0]

        # Filtering out tagged usernames for simplicity
        usernames = {user for user in usernames if not user.startswith("@MS4") and user != postCreator}

        with open(self.dataFile, "r") as file:
            data: dict[str: dict[str: list[str]]] = json.load(file)

        # Creator
        if postCreator in data.keys():
            data[postCreator]["connections"] = list( set(data[postCreator]["connections"]).union(usernames) )
            data[postCreator]["commenters"] = list( set(data[postCreator]["commenters"]).union(usernames) )
            data[postCreator]["hashtags"] = list( set(data[postCreator]["hashtags"]).union(hashtags) )
        else:
            data[postCreator] = {
                "connections": list(usernames),
                "commenters": list(usernames),
                "hashtags": list(hashtags)
            }

        # All users except Creator
        for user in usernames:
            adjustedUsers = usernames.copy()
            adjustedUsers.remove(user)
            adjustedUsers.add(postCreator)
            if user in data.keys():
                data[user]["connections"] = list( set(data[user]["connections"]).union(adjustedUsers) )
                data[user]["hashtags"] = list( set(data[user]["hashtags"]).union(hashtags) )
            else:
                data[user] = {
                    "connections": list(adjustedUsers),
                    "commenters": [],
                    "hashtags": list(hashtags)
                }

        with open(self.dataFile, "w") as file:
            json.dump(data, file, indent=3)

        self.__storeHashtagStatistics(hashtags)

    def parseDirectoryCommentsData(self, source: str) -> None:
        """
        Function gets all the filenames from a directory and calls the parseCommentsData function.

        Important: the func ignores filenames starting with "--"

        :param source:
        :return:
        """

        # TODO
        pass

    def __getDataFromFile(self, filename: str) -> (set, set):
        """
        Function reads the provided file and discerns the hashtags and usernames from it

        Source file should be .txt with format hashtags and usernames each in a new line. There should be
        an empty line separating the two sections.

        :param filename: name of the source file
        :return: Sets containing hashtags and usernames respectively
        """
        with open(filename, encoding="UTF-8") as f:
            data = f.read().strip().split("\n\n")

            hashtags = set(data[0].split("\n"))
            usernames = set(data[1].split("\n"))

            return hashtags, usernames

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