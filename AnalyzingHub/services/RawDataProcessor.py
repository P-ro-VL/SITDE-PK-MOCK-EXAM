from datetime import datetime


def process(id, data):
    args = data.split("&")
    data = {}
    for s in args:
        args2 = s.split("=")
        data[args2[0]] = args2[1]
    return ExamData(id, data)


class ExamData:
    def __init__(self, id, data):
        self.id = id
        timeFormat = "%H:%M:%S %d/%m/%Y"
        self.starting_date = datetime.strptime(data["StartingDate"].replace("-", "/"), timeFormat)
        self.submiting_date = datetime.strptime(data["SubmitingDate"].replace("-", "/"), timeFormat)
        self.score_10 = data["Score10"]
        self.tds = data["TDS"]
        self.code = data["Code"]

    def score_4(self):
        return (float(self.score_10.replace(",", ".")) / 10) * 4

    def total_doing_time(self):
        return (self.submiting_date - self.starting_date).seconds / 60  # In minutes
