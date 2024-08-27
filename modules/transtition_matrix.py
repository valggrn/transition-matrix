import numpy

class TransitionMatrix:
    """
    класс, реализующий генерацию текста с помощью цепей маркова
    """
    def __init__(self, corpus, length_prefix):
        """ инициализация класса """
        if len(corpus) == 0:
            print("Длина корпуса не может быть равна 0")
            exit(1)
        try:
            length_prefix = int(length_prefix)
        except ValueError:
            print("Длина префикса должна быть числом")
            exit(1)
        if length_prefix < 1:
            print("Длина префикса должна быть больше 0")
            exit(1)
        elif length_prefix >= len(corpus):
            print("Длина префикса не может равняться количеству слов исходного текста")
            exit(1)
        self.corpus = corpus
        self.length_prefix = length_prefix
        self.prefixes = None
        self.matrix = None

    def create_prefixes(self):
        """
        формирование пар префикс - суффикс из разбитого на слова исходного текста
        """
        self.first_prefix = None
        self.prefixes = {}
        for index in range(0, len(self.corpus) - self.length_prefix + 1):
            prefix = tuple(self.corpus[index:index + self.length_prefix])
            if len(self.corpus) <= index + self.length_prefix:
                suffix = None
            else:
                suffix = self.corpus[index + self.length_prefix]
            self.add_prefix(prefix, suffix)
            if self.first_prefix == None:
                self.first_prefix = prefix
        return self.prefixes
    
    def add_prefix(self, prefix, suffix):
        """
        сохранение количества суффиксов с определенным префиксом в словарь
        """
        if prefix not in self.prefixes:
            self.prefixes[prefix] = {}
        if suffix not in self.prefixes[prefix]:
            self.prefixes[prefix][suffix] = 0
        self.prefixes[prefix][suffix] += 1

    def make_matrix(self):
        """
        построение матрицы перехода
        """
        if self.prefixes == None:
            self.create_prefixes()
        self.matrix = {}
        for prefix, suffixes in self.prefixes.items():
            total_count = sum(suffixes.values())
            self.matrix[prefix] = {suffix: count / total_count for suffix, count in suffixes.items()}
        return self.matrix

    def generate_text_by_matrix(self):
        """
        генерация текста с помощью матрицы перехода
        """
        if self.matrix == None:
            self.make_matrix()
        current_prefix = self.first_prefix
        result = list(current_prefix)
        while(True):
            suffixes = list(self.matrix[current_prefix].keys())
            probabilities = list(self.matrix[current_prefix].values())
            suffix = numpy.random.choice(suffixes, p=probabilities)
            if suffix == None:
                break
            else:
                result.append(str(suffix))
            current_prefix = tuple(list(current_prefix[1:]) + [suffix])
        return result