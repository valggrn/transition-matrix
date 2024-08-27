import re
    
class File:
    def get_data_from_file(path):
        try:
            with open(path, 'r', encoding='utf-8') as openedFile:
                return openedFile.read()
        except IOError:
            print(f"could not read file at {path}")
            exit(1)

    def split_data(data):
        splitedData = []
        for word in data.split(" "):
            if len(word) != 0:
                splitedData.append(re.sub(r'[\r\n]+', '', word))
        return splitedData