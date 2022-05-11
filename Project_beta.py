import sys
import random
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QPushButton, QGroupBox, QRadioButton,
                             QVBoxLayout, QHBoxLayout, QButtonGroup, QMessageBox)
from Class import Question, User

# Это крч для, ну это, это нужно
from styles import bashkirenergo as style_1
from styles import mts as style_2
from styles import segezha_group as style_3
from styles import steppe as style_4

style = style_1    # Это необходимо

# Создание приложения и главного окна
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Тестирование")
window.resize(450, 200)

# Создание виджетов главного окна
question = QLabel("Выберите тест")
question.setWordWrap(True)

title_test = QLabel("Тестирование")

test_text = QLabel("Проверка эрудиции")
very_important_btn = QPushButton("Пройти тест")
btn_answer = QPushButton("Выбрать тест")
btn_quite = QPushButton("Закончить тест")


box_with_result = QGroupBox("Результат теста")

box_with_answers = QGroupBox("Варианты ответов")

pixmap = QPixmap(f"logo/{style.logo}")
logo = QLabel()
logo.resize(pixmap.width(), pixmap.height())
logo.setPixmap(pixmap)

# Создание кнопок и привязка их к группе
btn_1 = QRadioButton('ООО «Башкирэнерго»')
btn_2 = QRadioButton('МТС')
btn_3 = QRadioButton('Segezha Group')
btn_4 = QRadioButton('Агрохолдинг «СТЕПЬ»')

radio_group = QButtonGroup()

radio_group.addButton(btn_1)
radio_group.addButton(btn_2)
radio_group.addButton(btn_3)
radio_group.addButton(btn_4)

radio_group.answers = radio_group.buttons()

# Создание линий группы и привязка к ним виджетов
right_group_line = QVBoxLayout()
left_group_line = QVBoxLayout()
central_h_line = QHBoxLayout()

right_group_line.addWidget(btn_1, alignment=Qt.AlignVCenter)
right_group_line.addWidget(btn_2, alignment=Qt.AlignVCenter)
left_group_line.addWidget(btn_3, alignment=Qt.AlignVCenter)
left_group_line.addWidget(btn_4, alignment=Qt.AlignVCenter)
central_h_line.addLayout(right_group_line)
central_h_line.addLayout(left_group_line)
box_with_answers.setLayout(central_h_line)

# Создание Вертикально линии и привязка к ним группы вопросов
vertical_box_line = QVBoxLayout()
box_with_result.setLayout(vertical_box_line)

# Создание линий главного окна
main_line = QVBoxLayout()
up_mid_line = QHBoxLayout()
up_down_line = QHBoxLayout()
mid_line = QHBoxLayout()
down_line = QHBoxLayout()

# Привязка виджетов к главному окну
up_mid_line.addWidget(title_test, alignment=Qt.AlignLeft | Qt.AlignBottom)
up_mid_line.addWidget(logo, alignment=Qt.AlignRight)
up_down_line.addWidget(question)

mid_line.addWidget(box_with_answers)
mid_line.addWidget(box_with_result)
mid_line.addWidget(test_text, alignment=Qt.AlignCenter)
down_line.addWidget(btn_answer, stretch=2)
down_line.addWidget(btn_quite, stretch=2)
down_line.addWidget(very_important_btn, stretch=2)

main_line.addLayout(up_mid_line, stretch=2)
main_line.addLayout(up_down_line, stretch=1)
main_line.addLayout(mid_line, stretch=3)
main_line.addLayout(down_line, stretch=2)
window.setLayout(main_line)

# Прячем виджеты
question.hide()
btn_answer.hide()
box_with_result.hide()
box_with_answers.hide()
btn_quite.hide()
logo.hide()


# Функции
def hide():
    question.hide()
    btn_answer.hide()
    box_with_result.hide()
    box_with_answers.hide()
    btn_quite.hide()
    logo.hide()
    title_test.hide()


def show():
    question.show()
    box_with_answers.show()
    logo.show()
    title_test.show()


def chose_test():               # Выбор теста
    global style                # Вынужденная мера
    if btn_answer.text() == "Выбрать тест" and any([btn.isChecked() for btn in radio_group.buttons()]):
        if radio_group.answers[0].isChecked():
            style = style_1
        if radio_group.answers[1].isChecked():
            style = style_2
        if radio_group.answers[2].isChecked():
            style = style_3
        if radio_group.answers[3].isChecked():
            style = style_4
        settings_styles()
    try:
        start_test()
    except:
        pass


def settings_styles():
    global list_question
    global user
    logo.resize(pixmap.width(), pixmap.height())
    logo.setPixmap(QPixmap(f"logo/{style.logo}"))
    logo.show()

    window.resize(style.win_width, style.win_height)
    window.setStyleSheet(style.background)
    question.setStyleSheet(style.q_text_style)
    title_test.setStyleSheet(style.header_text_style)
    box_with_result.setStyleSheet(style.result_group_style)
    box_with_answers.setStyleSheet(style.radio_group_style)

    [btn.setStyleSheet(style.radiobutton_style) for btn in radio_group.buttons()]

    btn_answer.setText("Следующий вопрос")
    btn_answer.setFixedSize(225, 60)
    btn_quite.setFixedSize(225, 60)

    list_question, title = Question.generate_list_question(style.file_name)
    user = User(questions_num=(len(list_question)))

    title_test.setText(title)


def start():
    very_important_btn.hide()

    btn_quite.hide()
    test_text.hide()
    question.show()
    box_with_answers.show()
    btn_answer.show()
    btn_answer.setText("Выбрать тест")


def start_test():
    if btn_answer.text() == "Следующий вопрос" and box_with_result.isHidden() and any([btn.isChecked() for btn in radio_group.buttons()]) and len(list_question) != 0:
        check_answer()
        if len(list_question) == 0:
            btn_answer.setText("Выбрать другой тест")
        else:
            btn_answer.setText("Следующий вопрос")
        drop_flags()
        matter = chose_question(list_question)
        set_question(matter)

        print(matter)

    elif len(list_question) == 0 and btn_answer.text() != "Выбрать тест":
        drop_flags()
        check_answer()
        show_result()
        btn_answer.setText("Выбрать другой тест")
        btn_quite.show()
        hide()
        window.setStyleSheet(None)
        [btn.setStyleSheet(None) for btn in radio_group.buttons()]
        question.setStyleSheet(None)
        very_important_btn.setFixedSize(225, 60)
        very_important_btn.setText("Пройти другой тест")
        if btn_answer.text() == 'Выбрать другой тест':
            radio_group.answers[0].setText('ООО «Башкирэнерго»')
            radio_group.answers[1].setText('МТС')
            radio_group.answers[2].setText('Segezha Group')
            radio_group.answers[3].setText('Агрохолдинг «СТЕПЬ»')
            very_important_btn.show()
            question.setText("Выберите тест")
            btn_quite.show()


def chose_question(question_list: list):

    random.shuffle(question_list)
    return question_list.pop()


def set_question(matter: Question):
    question.setText(matter.qustion)
    random.shuffle(radio_group.answers)
    radio_group.answers[0].setText(matter.right_answer)
    radio_group.answers[1].setText(matter.wrong1)
    radio_group.answers[2].setText(matter.wrong2)
    radio_group.answers[3].setText(matter.wrong3)


def drop_flags():
    radio_group.setExclusive(False)
    for btn in radio_group.buttons():
        btn.setChecked(False)
    radio_group.setExclusive(True)


def check_answer():
    if radio_group.answers[0].isChecked():
        user.counter += 1
        print(user.counter)


def show_result():
    message = QMessageBox()
    message.resize(200, 200)
    message.move(800, 400)
    message.setWindowTitle("Результаты теста")
    message.setText(f"Ваш результат {user.counter} из {user.question_num}")
    message.exec_()


def quite():
    app.quit()


# Запуск программмы
btn_answer.clicked.connect(chose_test)
very_important_btn.clicked.connect(start)
btn_quite.clicked.connect(quite)
box_with_result.hide()
window.show()
app.exec_()
