# from urllib import request
# import yaml
#
# def parseType(raw):
#     if raw == "DC":
#         return "Đại cương"
#     elif raw == "CSN":
#         return "Cơ sở ngành"
#     elif raw == "CN":
#         return "Chuyên ngành"
#
# configURL = "https://raw.githubusercontent.com/P-ro-VL/SITDE-PK-BANKS/main/Data/SubjectCodes.yml"
# response = request.urlopen(configURL)
# config = response.read().decode("utf8")
#
# yamlConfig = yaml.safe_load(config)
#
# data = {}
# for subjectId in yamlConfig["Available"].keys():
#     oldData = yamlConfig["Available"][subjectId]
#     subjectData = {}
#     subjectData["Name"] = oldData["Name"]
#     subjectData["Enable"] = oldData["Enable"]
#     subjectData["Type"] = parseType(oldData["Type"])
#     subjectData["URL"] = {}
#     subjectData["URL"]["ReviewProposal"] = oldData["Theory"]
#
#     chapters = {}
#     index = 1
#     for _ in oldData["Questions"].keys():
#         nameData = oldData["Questions"][_]["Name"].split(" - ")
#         chapterData = {"Title": nameData[0],
#                        "Name": nameData[-1], "Time": oldData["Questions"][_]["Time"],
#                        "NQuestions": oldData["Questions"][_]["Count"],
#                        "HasExplanation": oldData["Questions"][_]["HasExplanation"],
#                        "FileName": oldData["Questions"][_]["FileName"]}
#         chapters[index] = chapterData
#         index += 1
#     subjectData["Chapters"] = chapters
#
#     data[subjectId] = subjectData
#
# print(data)
# with open('configure.yml', 'w', encoding="utf-8") as file:
#     yaml.dump(data, file, allow_unicode=True)
import os
import urllib
from urllib import request

import requests
import yaml
import validators
import pybase64


def fetchImage(rawData):
    if validators.url(rawData) == True:
        downloadImage(rawData)
        return imageToBase64().decode("utf8")
    else:
        return rawData


def imageToBase64():
    with open("tempPic.png", "rb") as img_file:
        my_string = pybase64.b64encode(img_file.read())
        return my_string


def downloadImage(url):
    with open('tempPic.png', 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)


configURL = "https://raw.githubusercontent.com/P-ro-VL/SITDE-PK-BANKS/main/Data/SubjectCodes.yml"
response = request.urlopen(configURL)
config = response.read().decode("utf8")

yamlConfig = yaml.safe_load(config)

for subjectId in yamlConfig["Available"].keys():
    print("Fetching " + subjectId + " ...")

    oldData = yamlConfig["Available"][subjectId]
    name = oldData["Name"]
    chapters = {}
    index = 1
    for _ in oldData["Questions"].keys():
        print("\tDeserializing " + _ + " ...")
        hasExplanation = oldData["Questions"][_]["HasExplanation"]
        fileName = oldData["Questions"][_]["FileName"]
        style = oldData["Questions"][_]["Style"]

        offset = 0
        if hasExplanation: offset = 1

        data = []

        url = "raw.githubusercontent.com/P-ro-VL/SITDE-PK-BANKS/main/" + name + "/" + fileName
        _response = request.urlopen("https://" + urllib.parse.quote(url))
        rawQuestion = _response.read().decode("utf8")

        splittedData = rawQuestion.split("<br>")
        if style == "SIMPLE_SELECT":
            newSplittedData = []
            for q in range(0, len(splittedData), 2 + offset):
                try:
                    newSplittedData.append(fetchImage(splittedData[q].replace("\n", "")))
                    newSplittedData.append("Đáp án A")
                    newSplittedData.append("Đáp án B")
                    newSplittedData.append("Đáp án C")
                    newSplittedData.append("Đáp án D")
                    newSplittedData.append(splittedData[q + 1])
                    if offset == 1:
                        newSplittedData.append(splittedData[q + 2])
                except:
                    continue
            splittedData = newSplittedData
        elif style == "IMAGE_QUESTION":
            for q in range(0, len(splittedData), 5 + offset):
                splittedData[q] = fetchImage(splittedData[q].replace("\n", ""))

        toWrite = "<br>".join(splittedData)

        print("\t\tWriting to file ...")

        os.makedirs(name, exist_ok=True)
        with open(name + "/" + fileName, "w", encoding="utf8") as f:
            f.write(toWrite)

print("Finished.")
