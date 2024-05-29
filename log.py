import json

class Log:
    def __init__(self, filename):
        self.filename = filename
        self.data_array = []

    def write(self, data):
        self.data_array.append(data)

    def save(self):
        with open(self.filename, "w") as file:
            file.write("[\n")
            for i, data in enumerate(self.data_array):
                if i > 0:
                    file.write(",\n")
                file.write("\t")
                file.write(json.dumps(data))
            file.write("\n]")