class Course:
    def __init__(self, title, classes):
        self.code = title.split(" ")[1]
        self.category = title.split(" ")[0]
        self.title = ""
        for i, w in enumerate(title.split(" ")[2:]):
            if (i == 0):
                self.title += w
            else:
                self.title += " " + w

        self.classes = classes