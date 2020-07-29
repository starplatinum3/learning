# 参考:
# https://blog.csdn.net/jia666666/article/details/81583129
# https://zhuanlan.zhihu.com/p/32134728
# https://www.cnblogs.com/ansang/p/7895075.html
# https://www.cnblogs.com/cxys85/p/10754309.html
# https://blog.csdn.net/paul200345/article/details/100826879
# https://blog.csdn.net/jia666666/article/details/81583129
# https://blog.csdn.net/rosefun96/article/details/79477974
# https://zhuanlan.zhihu.com/p/32134728
# https://www.cnblogs.com/ansang/p/7895075.html
# https://www.cnblogs.com/cxys85/p/10754309.html
# https://blog.csdn.net/paul200345/article/details/100826879
import os
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel, QPushButton, QTextEdit, QMessageBox, QWidget,
                             QTableWidget, QTableWidgetItem)
from PyQt5.QtGui import QPixmap, QFont

# https://blog.csdn.net/jia666666/article/details/81583129
from PyQt5.uic.properties import QtGui


class Form(QWidget):
    problems = []

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        font_yahei = QFont("Microsoft YaHei")
        self.setFont(font_yahei)
        self.parent = parent
        self.cnt_ans_img = 0
        self.dict_ans = None

        # name items

        self.lbl_msg = QLabel('messages here')
        lbl_input = QLabel("输入问题")
        lbl_input.setFont(QFont("Microsoft YaHei"))
        # https://blog.csdn.net/rosefun96/article/details/79477974
        # lbl_input.setStyleSheet("{font:'Courier New'}")
        lbl_input_ans = QLabel("输入答案")
        lbl_input_ans.setFont(QFont('Microsoft Yahei'))
        self.lbl_ans = QLabel('here is the answer')
        self.lbl_ans.setFont(font_yahei)
        btn_input_ans = QPushButton("从文本框录入答案")
        btn_input_ans_img = QPushButton("从剪贴板输入答案")
        btn_unshow_ans = QPushButton('unshow answer')
        btn_save = QPushButton('save')
        btn_modify_ans = QPushButton('modify ans')
        self.txt_input = QTextEdit(self)
        self.txt_input_ans = QTextEdit(self)
        btn_show_ans = QPushButton("show ans")

        btn_upgrade_tbl = QPushButton('upgrade table')

        self.window_tbl_problems=WindowListProblems(parent)
        ####
        self.window_tbl_problems.dialogSignel.connect(self.ans_to_problem)
# https://www.cnblogs.com/HE-helloword/articles/12347053.html
#         https://blog.csdn.net/caomin1hao/article/details/80388760
        self.window_tbl_problems.setGeometry(self.width()+700,self.depth()+100,300,1000)
# setGeometry (9,9, 50, 25) 从屏幕上(9,9)位置开始(即为最左上角的点),显示一个50*25的界面(宽50,高25

        # self.tbl_test = QTableWidget()
        # self.tbl_test.setRowCount(2)
        # self.tbl_test.setColumnCount(3)
        # self.test_put_picture() #table 不能放图片

        def problem_list_in_table():
            print('list the problems in table')
            row = 0
            col = 0
            for problem in self.problems:
                print("problem:")
                print(problem)
                self.window_tbl_problems.tbl_problems.setItem(row, col, QTableWidgetItem(problem))
                row += 1
            print('load done')

        # def init_list_problems():
        #     for problem in self.dict_ans:
        #         if not problem in self.problems:
        #             self.problems.append(problem)
        # init_list_problems()
        self.read_txt()
        problem_list_in_table()

        def set_layput():
            # 设置栅格布局，并添加部件到相应的位置
            layout = QGridLayout()

            layout.addWidget(self.lbl_msg,0,0)
            layout.addWidget(self.lbl_ans, 1, 0)
            layout.addWidget(lbl_input, 2, 0)
            layout.addWidget(lbl_input_ans, 2, 1)
            layout.addWidget(self.txt_input, 3, 0)
            layout.addWidget(self.txt_input_ans, 3, 1)
            layout.addWidget(btn_input_ans, 4, 0)
            layout.addWidget(btn_input_ans_img, 4, 1)
            layout.addWidget(btn_show_ans, 5, 0)
            layout.addWidget(btn_unshow_ans, 1, 2)
            layout.addWidget(btn_save, 6, 0)
            layout.addWidget(btn_modify_ans, 6, 1)

            layout.addWidget(btn_upgrade_tbl)
            layout.addWidget(self.lbl_msg)
            layout.addWidget(QPushButton('show list',self,clicked=self.show_list))

            # 设置主窗口的布局，自定义槽函数，设置标题
            self.setLayout(layout)

        set_layput()

        # connect
        btn_input_ans.clicked.connect(self.input_ans_txt)
        btn_show_ans.clicked.connect(self.show_ans)

        btn_input_ans_img.clicked.connect(self.input_ans_img)
        btn_unshow_ans.clicked.connect(self.unshow_ans)
        btn_save.clicked.connect(self.save)
        btn_modify_ans.clicked.connect(self.modify_ans)

        btn_upgrade_tbl.clicked.connect(self.upgrade_tbl)

        self.setWindowTitle("Learning")

    # https://zhuanlan.zhihu.com/p/32134728
    def show_list(self):
        self.window_tbl_problems.show()
        self.window_tbl_problems.setFocus()
    def test_put_picture(self):
        pix = QPixmap('image/img_ans/1.jpg')

        self.put_sth_at_table(pix, self.tbl_test)


    def put_sth_at_table(self, sth, table: QTableWidget):
        table.setItem(0, 0, item=QTableWidgetItem(sth))

    def put_ans_where(self, where: QWidget, problem: str):

        if not problem in self.dict_ans:
            self.lbl_ans.clear()
            self.msg('have no answer,please give an answer first')
            return
        ans = self.dict_ans[problem]
        print('ans:')
        print(ans)
        print('not ans:')
        print(not ans)

        if 'image/img_ans/' in ans:
            print('show image ans')
            print('path:')
            print(ans)
            pix = QPixmap(ans)
            # self.lbl_ans.setPixmap(pix)
            where.setPixmap(pix)
        else:

            self.msg('show text ans')
            # self.lbl_ans.setText(ans)
            where.setText(ans)

    def upgrade_tbl(self):
        print('list the problems into table')
        row = 0
        col = 0
        for problem in self.problems:
            print("problem:")
            print(problem)
            self.window_tbl_problems.tbl_problems.setItem(row, col, QTableWidgetItem(problem))
            row += 1
        print('load done')

    def ans_to_problem(self, problem: str):
        self.put_ans_where(self.lbl_ans, problem=problem)

    def msg(self, msg: str):
        print(msg)
        self.lbl_msg.setText(msg)

    def read_txt(self):
        print('loading...')
        self.lbl_msg.setText('loading...')
        file = open('dict_ans.txt', 'r')
        data = file.read()
        if not data:
            self.msg('dict_ans.txt 文件里什么都没有,现在要初始化这个文件')
            file.close()
            init_txt()

            self.msg('init done')
            file = open('dict_ans.txt', 'r')
            data = file.read()
        import ast

        dic = ast.literal_eval(data)
        self.dict_ans = dic['dict_ans']

        cnt_ans_img = dic['img_ans already']
        self.cnt_ans_img = cnt_ans_img
        if not 'problems' in dic:

            self.msg('have no problems, please input')
        else:
            self.problems = dic['problems']
            print('problems:')
            print(self.problems)

        file.close()
        print('load done')
        self.lbl_msg.setText('load done')

    def show_img(self):
        pix = QPixmap("image/img_ans/2.jpg")
        self.imageLabel.setPixmap(pix)

    def save_img(self):
        print('save img')
        clipboard = QApplication.clipboard()
        img = clipboard.pixmap()
        path = 'image/2.jpg'
        img.save(path)
        print('save at {}'.format(path))

    def input_ans_txt(self):
        # https://www.cnblogs.com/ansang/p/7895075.html
        problem = self.txt_input.toPlainText()
        if not problem in self.problems:
            self.problems.append(problem)
        if problem in self.dict_ans:
            self.msg('already have this problem')
            return
        ans = self.txt_input_ans.toPlainText()
        if ans == '':
            self.msg('没有答案，请输入问题再点击输入')
            return
        print("ans:")
        print(ans)
        self.dict_ans[problem] = ans

        self.msg('ans load done')

    def input_ans_img(self):

        self.msg('input a image ans')
        problem = self.txt_input.toPlainText()
        if not problem in self.problems:
            self.problems.append(problem)

        if problem in self.dict_ans:
            self.msg('already have this problem')
            return
        clipboard = QApplication.clipboard()

        img_ans = clipboard.pixmap()
        if not img_ans:
            self.msg('没有答案，请输入问题再点击输入')
            return
        path = 'image/img_ans/{}.jpg'.format(self.cnt_ans_img)
        img_ans.save(path)
        self.dict_ans[problem] = path
        self.cnt_ans_img += 1
        # self.imageLabel.setPixmap(self.dict_ans[problem])

        self.msg('ans load done')

    def show_ans(self):
        # _translate = QtCore.QCoreApplication.translate
        problem = self.txt_input.toPlainText()
        self.ans_to_problem(problem)

    def save(self):

        self.msg('saving..')
        path = 'dict_ans.txt'
        file = open(path, 'w')
        dic = {'img_ans already': self.cnt_ans_img, 'dict_ans': self.dict_ans, 'problems': self.problems}

        file.write(str(dic))
        file.close()

        self.msg('save done')

    def closeEvent(self, event):
        print('close')
        self.lbl_msg.setText('close')
        self.save()

    def unshow_ans(self):
        print('unshow ans')
        self.lbl_msg.setText('unshow ans')
        self.lbl_ans.clear()

    def modify_ans(self):
        print('messagebox')
        # https://www.cnblogs.com/cxys85/p/10754309.html
        # QMessageBox.addAction('text',action=self.modify_text)
        self.win_choose = Window(parent=self.parent)
        self.win_choose.resize(500, 200)
        self.win_choose.setWindowTitle('choose type of answer')
        # https://blog.csdn.net/paul200345/article/details/100826879
        self.win_choose.dialogSignel.connect(self.change_param)
        print('win show:')
        self.win_choose.show()

    def modify_text(self):
        problem = self.txt_input.toPlainText()
        ans = self.txt_input_ans.toPlainText()

    def change_param(self, choice: str):
        print('change param')
        print('signal:')
        print("choice: ")
        print(choice)
        problem = self.txt_input.toPlainText()
        if not problem:
            print('没有问题，请输入问题再点击输入')
            self.lbl_msg.setText('没有问题，请输入问题再点击输入')
            return
        if choice == 'text':
            ans = self.txt_input_ans.toPlainText()
            if ans == '':
                print('没有答案，请输入答案再点击输入')
                self.lbl_msg.setText('没有问题，请输入问题再点击输入')
                return
            print('ans:')
            print(ans)
            self.dict_ans[problem] = ans
        else:
            clipboard = QApplication.clipboard()
            img_ans = clipboard.pixmap()
            if not img_ans:
                print('没有答案，请输入答案再点击输入')
                self.lbl_msg.setText('没有问题，请输入问题再点击输入')
                return

            if not problem in self.dict_ans:
                print('原来没有相应的答案，现在是添加新的答案')
                self.lbl_msg.setText('原来没有相应的答案，现在是添加新的答案')
                path = 'image/img_ans/{}.jpg'.format(self.cnt_ans_img)
                img_ans.save(path)
                self.dict_ans[problem] = path
                self.cnt_ans_img += 1
            else:
                path_original = self.dict_ans[problem]
                print('修改答案')
                self.lbl_msg.setText('修改答案')
                img_ans.save(path_original)


class Window(QWidget):
    dialogSignel = pyqtSignal(str)

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        btn_text = QPushButton('text')
        btn_img = QPushButton('image')

        layout = QGridLayout()
        layout.addWidget(btn_text, 0, 0)
        layout.addWidget(btn_img, 0, 1)
        self.setLayout(layout)
        btn_text.clicked.connect(self.choose_text)
        btn_img.clicked.connect(self.choose_img)

    def choose_text(self):
        print('choose text')
        self.choose = self.text
        self.dialogSignel.emit('text')
        print('close')
        self.close()

    def choose_img(self):
        print('choose image')
        self.choose = self.img
        self.dialogSignel.emit('img')
        print('close')
        self.close()

    def closeEvent(self, event) -> None:
        print('close')

    text = 0
    img = 1
    choose = 0

class WindowListProblems(QWidget):
    dialogSignel = pyqtSignal(str)

    def __init__(self, parent=None):
        super(WindowListProblems, self).__init__(parent)
        self.setWindowTitle('list problems')
        self.tbl_problems=QTableWidget(clicked=self.send_problem)
        self.tbl_problems.setColumnCount(1)
        self.tbl_problems.setRowCount(10)
        self.resize(300,1000)
        layout=QGridLayout()
        layout.addWidget(self.tbl_problems)
        self.setLayout(layout)

    def get_problem(self):
        row_index = self.tbl_problems.currentIndex().row()  # 获取当前行 index
        if self.tbl_problems.item(row_index, 0):
            problem = self.tbl_problems.item(row_index, 0).text()  # item(行,列), 获取当前行
            print("problem:")
            print(problem)
            # self.ans_to_problem(problem)
            return problem

    def send_problem(self):
        problem=self.get_problem()
        self.dialogSignel.emit(problem)
def init_txt():
    dic = {'img_ans already': 0}
    ans = {'1+1': '2'}
    problems = ['1+1']
    dic['dict_ans'] = ans
    dic['problems'] = problems

    file = open('dict_ans.txt', 'w')
    file.write(str(dic))
    file.close()


def look_dic():
    dic = {'img_ans already': 0}
    ans = {'1+1': '2'}
    problems = ['1+1']
    dic['dict_ans'] = ans
    dic['problems'] = problems
    print(str(dic))


def build():
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())


build()
