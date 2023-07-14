# Công cụ phân tích dữ liệu của kỳ thi thử HIỆN TẠI trên SITDE-PK-Mock-Exam firebase project
import os

import firebase_admin
import numpy
from firebase_admin import firestore
from firebase_admin import credentials
from services import RawDataProcessor
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

credential = credentials.Certificate("service_account.json")
app = firebase_admin.initialize_app(credential=credential)
db = firestore.client()

colRef = db.collection("mock-exam-history")
docs = colRef.stream()

participatingAmount = 0
loadedData = []

for doc in docs:
    participatingAmount += 1
    dictionary = doc.to_dict()

    for v in dictionary.values():
        try:
            data = RawDataProcessor.process(doc.id, v)
            loadedData.append(data)
        except:
            print("Could not load " + doc.id)
            continue

print(len(loadedData))

###########################################################
# INTERACTABLE SECTION START HERE
###########################################################
codes = []
for d in loadedData:
    rawcode = d.code.split("_")[0]
    if not(rawcode in codes):
        codes.append(rawcode)

for viewingCode in codes:
    outDir = "output/" + viewingCode + "/"
    try:
        os.mkdir(outDir)
    except:
        print("Folder has been existed.")

    ids = []
    codes = []
    startDates = []
    submitDates = []
    totalTimes = []
    score10s = []
    score4s = []
    tds = []

    for d in loadedData:
        if viewingCode in d.code:
            ids.append(d.id)
            codes.append(d.code)
            startDates.append(d.starting_date)
            submitDates.append(d.submiting_date)
            totalTimes.append(d.total_doing_time())
            score10s.append(d.score_10)
            score4s.append(d.score_4())
            tds.append(d.tds)

    df = pd.DataFrame()
    df["ID"] = ids
    df["CODE"] = codes
    df["STARTING DATE"] = startDates
    df["SUBMITING DATE"] = submitDates
    df["TOTAL TIME"] = totalTimes
    df["SCORE 10"] = score10s
    df["SCORE 4"] = score4s
    df["TDS"] = tds

    df.set_index("ID")

    print("Participating Amount: " + str(participatingAmount))
    print(df)
    print("Viewing Code: " + viewingCode)
    df.to_excel(outDir + viewingCode + ".xlsx")

    plt.figure(figsize=[13.33, 7.5])
    ar = Counter(df["SCORE 4"].sort_values().map(lambda x: str(x)))
    plt.bar(ar.keys(), ar.values())
    plt.xlabel("Điểm trung bình: " + str(numpy.average(df["SCORE 4"])))
    plt.title("PHỔ ĐIỂM HỆ 4 MÃ HỌC PHẦN " + viewingCode + " (" + str(len(ids)) + " người tham gia)")
    plt.savefig(outDir + "Phổ điểm hệ 4.png")

    plt.clf()

    ar = Counter(df["SCORE 10"].map(lambda x: float(x.replace(",", ".")))
                 .sort_values().map(lambda x: str(x)))
    plt.bar(ar.keys(), ar.values())
    plt.xlabel("Điểm trung bình: " + str(numpy.average(df["SCORE 10"].map(lambda x: float(x.replace(",", "."))))))
    plt.title("PHỔ ĐIỂM HỆ 10 MÃ HỌC PHẦN " + viewingCode + " (" + str(len(ids)) + " người tham gia)")
    plt.savefig(outDir + "Phổ điểm hệ 10.png")

    plt.clf()
