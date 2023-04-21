import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PyQt6.QtCore import QSize, QRect
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6 import QtGui
from gensim.models import Word2Vec
from modelvec import similarity, visualization, setEdges_simWords

model = Word2Vec.load('word2vec-TeenInstagram.model')


class Home(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
        self.setFixedSize(QSize(768, 402))
        self.show()

    def initUI(self):
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap("/Users/minseokey/Kookmin/BDLT/Project/BDLT_Project/static/즐겁다 마참내.png"))
        self.label.setGeometry(QRect(0, 0, 768, 402))
        self.titletext = QLabel(self)
        self.titletext.setText("MZ 세대의 선택은?")  # 텍스트 변환
        self.titletext.setFont(QtGui.QFont("", 20))  # 폰트,크기 조절
        self.titletext.setStyleSheet("Color : black")  # 글자색 변환
        self.titletext.move(300, 35)
        self.lbl1 = QLabel('키워드는 무엇인가요?', self)
        self.lbl1.setStyleSheet('Color : black')
        self.lbl1.move(220, 100)
        self.lbl2 = QLabel('첫번째 아이템은 무엇인가요?', self)
        self.lbl2.setStyleSheet('Color : black')
        self.lbl2.move(220, 150)
        self.lbl3 = QLabel('두번째 아이템은 무엇인가요?', self)
        self.lbl3.setStyleSheet('Color : black')
        self.lbl3.move(220, 200)

        self.input1 = QLineEdit(self)
        self.input1.move(420, 100)
        self.input2 = QLineEdit(self)
        self.input2.move(420, 150)
        self.input3 = QLineEdit(self)
        self.input3.move(420, 200)

        self.btn = QPushButton('정말 궁금해요!', self)
        self.btn.setStyleSheet('Color : black')
        self.btn.move(320, 250)
        self.btn.clicked.connect(self.submit)

        self.btntext = QLabel('이 키워드는 어떤 분포를 가질까?', self)
        self.btntext.setStyleSheet('Color : black')
        self.btntext.move(220, 320)

        self.btn1 = QPushButton('분포를 볼까요?', self)
        self.btn1.setStyleSheet('Color : black')
        self.btn1.move(420, 313)
        self.btn1.clicked.connect(self.showNetwork)

        self.setGeometry(300, 300, 250, 200)

    def submit(self):
        input1_text = self.input1.text().strip()
        input2_text = self.input2.text().strip()
        input3_text = self.input3.text().strip()
        try:
            ret1 = similarity(input1_text, input2_text, input3_text, model)
            matplotlib.rc('font', family="Nanum Gothic")
            matplotlib.rcParams['axes.unicode_minus'] = False
            x = np.arange(2)
            plt.figure(figsize=(3, 3), dpi=80)
            plt.bar(x, ret1, color="C2", width=0.4)
            plt.xticks(x, [input2_text, input3_text], size="20")
            plt.ylabel("유사도")
            plt.title("MZ 세대 " + input1_text + "의 트랜드는?")
            plt.savefig("static/graph.png")

            self.close()
            self.second = Result(ret1, input1_text, input2_text, input3_text)
            self.second.show()

        except:
            QMessageBox.about(self, "error!", "이런! 존재하지 않는 내용이에요!  다시 시도해주세요!")

    def showNetwork(self):
        keyword = self.input1.text().strip()
        visualization(setEdges_simWords(model,keyword),"static/newimage")
        self.close()
        self.third = Network(keyword)
        self.third.show()


class Result(QWidget):
    def __init__(self, ret, in1, in2, in3):
        super(Result, self).__init__()

        self.answerUI(ret, in1, in2, in3)
        self.setFixedSize(QSize(768, 402))
        self.show()

    def answerUI(self, ret, in1, in2, in3):
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap("/Users/minseokey/Kookmin/BDLT/Project/BDLT_Project/static/즐겁다 마참내.png"))
        self.label.setGeometry(QRect(0, 0, 768, 402))

        self.label = QLabel(self)
        self.label.setPixmap(QPixmap("/Users/minseokey/Kookmin/BDLT/Project/BDLT_Project/static/graph.png"))
        self.label.setGeometry(QRect(120, 20, 768, 390))

        self.text = QLabel(self)
        self.text.setText("키워드는 " + in1 + "입니다!")
        self.text.setFont(QtGui.QFont("", 20))
        self.text.setStyleSheet('Color : black')
        self.text.move(325, 40)

        self.text1 = QLabel(self)
        self.text1.setText(in2 + " 의 가중치는 " + str(ret[0]) + " 입니다!")
        self.text1.setStyleSheet('Color : black')
        self.text1.move(405, 130)

        self.text2 = QLabel(self)
        self.text2.setText(in3 + " 의 가중치는 " + str(ret[1]) + " 입니다")
        self.text2.setStyleSheet('Color : black')
        self.text2.move(405, 180)

        temp = in2 if ret[0] > ret[1] else in3
        self.answer = QLabel(self)
        self.answer.setText(temp + " (이)가 MZ 트랜드 입니다! 야호!")
        self.answer.setStyleSheet('Color : black')
        self.answer.move(405, 230)

        self.home = QPushButton('돌아가기', self)
        self.home.setStyleSheet('Color : black')
        self.home.move(445, 290)
        self.home.clicked.connect(self.Return)
        self.setGeometry(300, 300, 250, 200)

    def Return(self):
        self.close()
        self.main = Home()
        self.main.show()


class Network(QWidget):
    def __init__(self,subject):
        super(Network,self).__init__()

        self.networkUI(subject)
        self.setFixedSize(QSize(768, 402))
        self.show()

    def networkUI(self,subject):
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap("/Users/minseokey/Kookmin/BDLT/Project/BDLT_Project/static/즐겁다 마참내.png"))
        self.label.setGeometry(QRect(0, 0, 768, 402))

        self.label = QLabel(self)
        self.label.setPixmap(QPixmap("/Users/minseokey/Kookmin/BDLT/Project/BDLT_Project/static/newimage.png"))
        self.label.setGeometry(QRect(0, 0, 768, 402))

        self.text = QLabel(self)
        self.text.setText("키워드는 " + subject + "입니다!")
        self.text.setFont(QtGui.QFont("", 20))
        self.text.setStyleSheet('Color : black')
        self.text.move(470, 80)

        self.home = QPushButton('돌아가기', self)
        self.home.setStyleSheet('Color : black')
        self.home.move(510, 300)
        self.home.clicked.connect(self.Return)

        self.setGeometry(300, 300, 250, 200)

    def Return(self):
        self.close()
        self.main = Home()
        self.main.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Home()
    sys.exit(app.exec())
