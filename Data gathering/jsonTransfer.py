import json
import os
import re

class DataParser:
    def __init__(self, dataFile: str, hashtagFile: str):
        self.dataFile: str = dataFile
        self.hashtagFile: str = hashtagFile

        self.parsedSourceFile: str = "parsedSources.txt"
        self.parsedSources = []

    def parseFileCommentsData(self, source: str) -> None:
        """
        Function reads the source file and creates connections between the creator and commenters,
        as well as storing the associated hashtags as well as comment text and the number of likes.
        :param source: source filename
        :return: None
        """

        usedSource = self.__removeSearchFromFilename(source)

        if self.__fileParsed(usedSource):
            return

        count: int
        hashtags: set[str]
        comments: set[tuple[str, str, int]]
        count, hashtags, comments = self.__getCommentsDataFromFile(usedSource)

        postCreator = usedSource.split("/")[-1].split("-")[0]

        filteredComments = set()
        usernames = set()
        for entry in comments:
            user, text, likes = entry

            usernames.add(user)
            filteredComments.add(entry)

        try:
            with open(self.dataFile, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}

        # Creator
        if postCreator in data.keys():
            data[postCreator]["commenters"] = list( set(data[postCreator]["commenters"]).union(usernames) )
            data[postCreator]["hashtags"] = list( set(data[postCreator]["hashtags"]).union(hashtags) )
            data[postCreator]["totalCommentsCount"] += count
            data[postCreator]["shownCommentsCount"] += len(filteredComments)
        else:
            data[postCreator] = {
                "totalFollowingCount" : 0,
                "shownFollowingCount" : 0,
                "following" : [],
                "totalFollowersCount": 0,
                "shownFollowersCount" : 0,
                "followers" : [],
                "totalCommentsCount" : count,
                "shownCommentsCount" : len(filteredComments),
                "commentedOn" : [],
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
                data[user]["commentedOn"] = list( set(data[user]["commentedOn"]).union(postCreator) )
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
                    "totalFollowingCount": 0,
                    "shownFollowingCount": 0,
                    "following": [],
                    "totalFollowersCount": 0,
                    "shownFollowersCount": 0,
                    "followers": [],
                    "totalCommentsCount": 0,
                    "shownCommentsCount": 0,
                    "commentedOn": [postCreator,],
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

        self.__noteParsedFile(usedSource)

    def parseDirectoryCommentsData(self, directory: str) -> None:
        """
        Function gets all the filenames from a directory and calls the parseFileCommentsData function.

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

    def __getCommentsDataFromFile(self, filename: str) -> (int ,set[str], set[tuple[str, str, int]]):
        """
        Function reads the provided file and discerns the hashtags and usernames/comments/likes from it

        Source file should be .txt with format hashtags each in a new line. There should be
        an empty line separating the two sections. The other section should be "@user$Comment$likes".

        :param filename: name of the source file
        :return: Int=total comments count, sets containing hashtags and tuples containing the rest of the data respectively
        """
        with open(filename, "r", encoding="UTF-8") as f:

            count = int(f.readline().strip())

            text = f.read()

        if text[:2] == "\n\n":
            hashtags = set()
            text = text[2:]
            commentsLines = text.split("\n")
        else:
            data = text.strip().split("\n\n")
            hashtags = set(data[0].split("\n"))
            commentsLines = data[1].split("\n")

        commentsLines = self.__cleanUpCommentsData(commentsLines)

        comments = set()

        for line in commentsLines:
            sep = line.split("$")

            sep[2] = self.__convertSimpleIntToInt(sep[2])

            try:
                hashtags.update(set(re.findall(r'#\w+', sep[1])))
            except:
                pass

            try:
                comments.add((sep[0], sep[1], sep[2]))
            except:
                comments.add((sep[0], sep[1], 0))

        return count, hashtags, comments

    def __cleanUpCommentsData(self, lines: list[str]) -> list[str]:
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

    def parseFileFollowsData(self, source: str) -> None:
        """
        Function parses through the file containing either Followers or Following with the site provided total amount
        :param source: File with name format "@name (type)" where type is Followers or Following
        :return: None
        """

        noPath: str = source.split("/")[-1]
        accountUser: str = noPath.split(" ")[0]
        fileType: str = noPath.split(" ")[1].replace(").txt", "").replace("(","")

        if fileType not in ["Followers","Following"]:
            raise NameError("File must be either (Followers) or (Following)")

        if self.__fileParsed(source):
            return

        count: int
        usernames: set[str]
        count, usernames = self.__getFollowsDataFromFile(source)

        if "" in usernames:
            usernames.remove("")

        try:
            with open(self.dataFile, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}

        if fileType == "Followers":
            if accountUser in data.keys():
                data[accountUser]["followers"] = list( set(data[accountUser]["followers"]).union(usernames) )
                data[accountUser]["totalFollowersCount"] = count
                data[accountUser]["shownFollowersCount"] = len(usernames)
            else:
                data[accountUser] = {
                    "totalFollowingCount": 0,
                    "shownFollowingCount": 0,
                    "following": [],
                    "totalFollowersCount": count,
                    "shownFollowersCount": len(usernames),
                    "followers": list(usernames),
                    "totalCommentsCount": 0,
                    "shownCommentsCount": 0,
                    "commentedOn": [],
                    "commenters": [],
                    "hashtags": [],
                    "commentsPosted": []
                }

            for followerUser in usernames:
                if followerUser == "":
                    continue
                if followerUser in data.keys():
                    if accountUser not in data[followerUser]["following"]:
                        data[followerUser]["following"].append(accountUser)
                        # Not total, accountUser should be counted in that already
                        # Not shown, that tells only what TikTok showed us
                else:
                    data[followerUser] = {
                        "totalFollowingCount": 0,
                        "shownFollowingCount": 0,
                        "following": [accountUser],
                        "totalFollowersCount": 0,
                        "shownFollowersCount": 0,
                        "followers": [],
                        "totalCommentsCount": 0,
                        "shownCommentsCount": 0,
                        "commentedOn": [],
                        "commenters": [],
                        "hashtags": [],
                        "commentsPosted": []
                    }

        elif fileType == "Following":
            if accountUser in data.keys():
                data[accountUser]["following"] = list(set(data[accountUser]["following"]).union(usernames))
                data[accountUser]["totalFollowingCount"] = count
                data[accountUser]["shownFollowingCount"] = len(usernames)
            else:
                data[accountUser] = {
                    "totalFollowingCount": count,
                    "shownFollowingCount": len(usernames),
                    "following": list(usernames),
                    "totalFollowersCount": 0,
                    "shownFollowersCount": 0,
                    "followers": [],
                    "totalCommentsCount": 0,
                    "shownCommentsCount": 0,
                    "commentedOn": [],
                    "commenters": [],
                    "hashtags": [],
                    "commentsPosted": []
                }

            for followingUser in usernames:
                if followingUser == "":
                    continue
                if followingUser in data.keys():
                    if accountUser not in data[followingUser]["followers"]:
                        data[followingUser]["followers"].append(accountUser)
                        # Not total, accountUser should be counted in that already
                        # Not shown, that tells only what TikTok showed us
                else:
                    data[followingUser] = {
                        "totalFollowingCount": 0,
                        "shownFollowingCount": 0,
                        "following": [],
                        "totalFollowersCount": 0,
                        "shownFollowersCount": 0,
                        "followers": [accountUser],
                        "totalCommentsCount": 0,
                        "shownCommentsCount": 0,
                        "commentedOn": [],
                        "commenters": [],
                        "hashtags": [],
                        "commentsPosted": []
                    }


        with open(self.dataFile, "w") as file:
            json.dump(data, file, indent=3)

        self.__noteParsedFile(source)

    def parseDirectoryFollowsData(self, directory: str) -> None:
        """
        Function gets all the filenames from a directory and calls the parseFileFollowsData function.

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

            self.parseFileFollowsData(f"{directory}/{file}")

    def __getFollowsDataFromFile(self, filename: str) -> (int, set[str]):
        """
        Function reads the provided file and discerns the number on the first line and creates a set from the rest from it
        :param filename: File with either Following or Followers
        :return: Total count from TikTok and a set of shown Users in the current category
        """
        with open(filename, "r", encoding="UTF-8") as file:

            count: int = self.__convertSimpleIntToInt(file.readline().strip())

            names = file.read().split("\n")

            return count, set(names)

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

    def __fileParsed(self, source: str) -> bool:
        """
        Checks whether the source file is parsed or not. Reads and notes the contents of the parsedPostsFile
        if we haven't yet accessed it.
        :param source: Path to the source file
        :return: True/False if the file has been parsed or not
        """

        if len(self.parsedSources) == 0:
            try:
                with open(self.parsedSourceFile, "r") as file:
                    self.parsedSources = file.read().split("\n")
            except FileNotFoundError:
                return False

        return source in self.parsedSources

    def __noteParsedFile(self, source: str) -> None:
        """
        Notes the current file so we don't have to parse over it unnecessarily. The information is remembered in
        the parsedPostsFile and as a class parameter, so we don't have to open a file everytime we want to check,
        thus making the process more efficient
        :param source: Path to the source file
        :return: None
        """
        if source in self.parsedSources:
            return

        with open(self.parsedSourceFile, "a") as file:
            file.write(source + "\n")

        self.parsedSources.append(source)

    def __removeSearchFromFilename(self, source: str) -> str:
        """
        Function to remove the search tag from the filenames that contain it
        :param source: Path to the source file
        :return: New source file name
        """

        newSource = source
        index = newSource.find("_q=")
        if index != -1:
            newSource = newSource[:index] + ".txt"
            os.rename(source, newSource)

        return newSource

    def __convertSimpleIntToInt(self, number: str) -> int:
        """
        Converts number in string form into an integer. Takes in mind the number might be in format "1.1M" or "6.8K"
        (Shouldn't be needed but kept for redundancy)
        :param number: String
        :return: Converted integer
        """
        if len(number) == 0:
            return 0

        dic = {
            "K": 1000.0,
            "M": 1_000_000.0
        }
        multiplier: str = number[-1]

        if multiplier in dic.keys():
            return int( float(number[:-1]) * dic[multiplier])
        else:
            return int(number)