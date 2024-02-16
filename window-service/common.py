import os


class commons:
    def __init__(self):
        super().__init__()
        pass

    def log(self, msg):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.dirArr = self.BASE_DIR.split("\\")
        self.dirArr.append("log.txt")
        self._ = "\\"
        self.logifilepath = self._.join(self.dirArr)
        with open(self.logifilepath, "a+") as file:
            file.write(msg + " \n")
        pass
