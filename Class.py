class Question:
    def __init__(self, question: str, right_answer: str,
                 wrong1: str, wrong2: str, wrong3: str):
        self.qustion = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

    @classmethod
    def generate_list_question(cls, path):
        with open(file=path, mode="r", encoding='utf8') as file:
            lines = [i.replace("\n", "") for i in file.readlines()]
            list_question = []
            title = lines.pop(0)

            while len(lines) != 0:
                list_question_cls = cls(lines[0], lines[1],
                                        lines[2], lines[3], lines[4])
                list_question.append(list_question_cls)
                del lines[0:5]
        return list_question, title


class User:
    def __init__(self, questions_num: int):
        self.question_num = questions_num
        self.counter = 0

