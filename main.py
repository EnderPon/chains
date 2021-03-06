from random import choices as choice


class Chain:
    def __init__(self):
        # self.punctuation = [".", ",", "!", "?", ":", ";", "'", '"', "(", ")", "-", "–", "\n"]
        self.punctuation = ["\n"]
        self.need_update = False  # показатель, что были изменения с момента последнего пересчёта весов
        self.list = {}
        return

    def add_rule(self, first, rule):
        self.need_update = True
        if first not in self.list:
            self.list[first] = {"sum": 1, "rules": {}}
        else:
            self.list[first]["sum"] += 1
        if rule in self.list[first]["rules"]:
            self.list[first]["rules"][rule]["count"] += 1
        else:
            self.list[first]["rules"][rule] = {}
            self.list[first]["rules"][rule]["count"] = 1

    def _update_weights(self):
        """Пересчитываем веса, если происходило обучение"""
        self.need_update = False
        for first in self.list:
            for key, value in self.list[first]["rules"].items():
                self.list[first]["rules"][key]["weight"] = value["count"]/self.list[first]["sum"]

    def next(self, prev):
        if self.need_update is True:
            self._update_weights()
        next_ = []
        weights = []
        if prev not in self.list:
            prev = "\n"
            #print(self.list.items())
            #prev = choice(self.list.items()[0])
            #print(prev)
        for rule in self.list[prev]["rules"]:
            next_.append(rule)
            weights.append(self.list[prev]["rules"][rule]["weight"])
        return choice(population=next_, weights=weights, k=1)[0]

    def teaching_file_letters(self, filename, letters):
        with open(filename, "r") as text:
            prev_letter = " "*letters
            while True:
                letter = text.read(letters)
                if letter == "":
                    break
                self.add_rule(prev_letter, letter)
                prev_letter = letter

    def teaching_file_words(self, filename):
        with open(filename, "r") as text:
            prev_word = ""
            word = ""
            count = 0
            while True:
                count += 1
                letter = text.read(1)
                if letter == "":
                    break
                if letter in self.punctuation:
                    self.add_rule(prev_word, word)
                    prev_word = word
                    self.add_rule(prev_word, letter)
                    prev_word = letter
                    word = ""
                elif letter == " ":
                    self.add_rule(prev_word, word)
                    prev_word = word
                    word = ""
                else:
                    word += letter

    def print(self):
        print(self.list)

def main():
    chain = Chain()
    chain.teaching_file_words("in")

    last = "\n"
    out = ""
    for i in range(1000):
        new = chain.next(last)
        out += ("" if new in chain.punctuation else " ") + new
        last = new
    print(out)

main()
