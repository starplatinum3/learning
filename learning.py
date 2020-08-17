# 参考:
# https://blog.csdn.net/jia666666/article/details/81583129
# https://blog.csdn.net/qq_40523737/article/details/81107089
# https://zhidao.baidu.com/question/2074168509029592828.html
# https://bbs.csdn.net/topics/392028741?page=1
# https://blog.csdn.net/jacke121/article/details/89338898
# https://blog.csdn.net/MAOZEXIJR/article/details/83111344
# https://www.dazhuanlan.com/2020/03/13/5e6ac5e82cf72/
# https://blog.csdn.net/rosefun96/article/details/79471674
# https://blog.csdn.net/rosefun96/article/details/79477974
# https://blog.csdn.net/wowocpp/article/details/105221265
# https://blog.csdn.net/caomin1hao/article/details/80388760
# https://www.cnblogs.com/archisama/p/5444032.html
# https://blog.csdn.net/weixin_45961774/article/details/106008803
# https://blog.csdn.net/dengnihuilaiwpl/article/details/90321249
# https://blog.csdn.net/Victor_zero/article/details/81268465?utm_source=blogxgwz9
# https://www.cnblogs.com/ansang/p/7895075.html
# https://www.cnblogs.com/cxys85/p/10754309.html
# https://blog.csdn.net/paul200345/article/details/100826879
# https://www.cnblogs.com/daisyyang/p/11138202.html
# https://blog.csdn.net/uuihoo/article/details/79496440
import os
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel, QPushButton, QTextEdit, QMessageBox, QWidget,
                             QTableWidget, QTableWidgetItem, QMenu, QInputDialog, QLineEdit)
from PyQt5.QtGui import QPixmap, QFont, QIcon, QCursor

# https://blog.csdn.net/jia666666/article/details/81583129
from PyQt5.uic.properties import QtGui


# https://blog.csdn.net/qq_40523737/article/details/81107089
def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
            print('not in')
        return _instance[cls]

    return inner


@singleton
class DataBase():
    info = {}
    problems = []
    lst_dic_exists = []
    dict_ans = {}
    cnt_ans_img = 0

    def __init__(self):
        print('init data base')

    def get_num_problems(self, path: str):
        return len(self.info[path])

    def get_dir_nums(self):
        return len(self.info) - 2  # 减去cnt_ans_img, problems


class Direction(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('dir')
        self.tbl_dir = TblToListItems()

        self.setFixedWidth(300)
        self.setFixedHeight(800)
        self.tbl_dir.clicked.connect(self.show_problems)
        self.put_dir_init()

        layout = QGridLayout()

        layout.addWidget(self.tbl_dir)
        layout.addWidget(QPushButton('refresh', clicked=self.put_dir_init))
        self.setLayout(layout)

    def put_dir_init(self):
        data_base = DataBase()
        not_put = ['img_ans already', 'problems']

        self.tbl_dir.put_items_to_tbl(data_base.info, not_put)

    def show_problems(self):
        txt_dir = self.tbl_dir.get_item_txt_from_tbl()
        data_base = DataBase()
        # self.tbl_dir.put_items_to_tbl(data_base.info[txt_dir])

        self.win_tbl_problems = WindowTableProblemsWithMove()

        self.win_tbl_problems.setGeometry(
            self.geometry().x() + self.width() + 10, self.geometry().y(), 300, 800)

        self.win_tbl_problems.setWindowTitle(txt_dir)
        if txt_dir == None:
            print('nothing to show')
            return

        self.win_tbl_problems.put_problems_and_answers(data_base.info[txt_dir])
        self.win_tbl_problems.move(
            self.geometry().x() + self.width() + 10, self.geometry().y())
        self.win_tbl_problems.show()


class WindowWithTblProblems(QWidget):
    def __init__(self):
        super().__init__()
        self.set_up_ui()

    def set_up_ui(self):
        font_yahei = QFont("Microsoft YaHei")
        self.setFont(font_yahei)
        self.tbl_problems = TblToListItems()

        self.tbl_problems.clicked.connect(self.show_ans)

        layout = QGridLayout()
        layout.addWidget(self.tbl_problems)
        self.btn_show = QPushButton('unshow ans')
        self.btn_show.clicked.connect(self.show_or_not)
        self.lbl_ans = QLabel('ans')
        layout.addWidget(self.lbl_ans)
        layout.addWidget(self.btn_show)

        self.setLayout(layout)

    def put_problems(self, problems):
        self.tbl_problems.put_items_to_tbl(problems)

    def show_or_not(self):
        if self.btn_show.text() == 'unshow ans':
            # https://zhidao.baidu.com/question/2074168509029592828.html
            self.btn_show.setText('show ans')
            self.tbl_problems.setColumnHidden(1, True)

            self.lbl_ans.clear()
        else:
            self.btn_show.setText('unshow ans')
            self.tbl_problems.setColumnHidden(1, False)

    def unshow_ans(self):
        # https://bbs.csdn.net/topics/392028741?page=1
        self.tbl_problems.setColumnHidden(1, True)

    def show_ans(self):

        # self.lbl_ans = QLabel('ans:')
        problem = self.get_problem()
        self.put_ans_where(self.lbl_ans, problem)
        print('ans show ')
        # self.lbl_ans.setWindowTitle('ans')

        # self.lbl_ans.show()

    def put_ans_where(self, where: QWidget, problem: str):
        data_base = DataBase()
        if problem not in data_base.dict_ans:
            self.lbl_ans.clear()
            print('have no answer,please give an answer first')
            return
        ans = data_base.dict_ans[problem]
        print('ans:')
        print(ans)

        if 'image/img_ans/' in ans:
            print('show image ans')
            print('path:')
            print(ans)
            pix = QPixmap(ans)
            # self.lbl_ans.setPixmap(pix)
            where.setPixmap(pix)
        else:

            # self.msg('show text ans')
            print('show text ans')
            # self.lbl_ans.setText(ans)
            where.setText(ans)

    def get_problem(self):
        return self.tbl_problems.get_item_txt_from_tbl()

    def put_problems_and_answers(self, problems):
        row = 0
        col = 0
        self.tbl_problems.setRowCount(len(problems))
        self.tbl_problems.setColumnCount(2)

        column_name = [
            'problem',
            'answer',
        ]
        self.tbl_problems.setHorizontalHeaderLabels(column_name)
        data_base = DataBase()
        for problem in problems:
            self.tbl_problems.setItem(row, 0, QTableWidgetItem(problem))
            self.tbl_problems.setItem(
                row, 1, QTableWidgetItem(data_base.dict_ans[problem]))
            row += 1


class WindowTableProblemsWithMove(WindowWithTblProblems):

    # https://blog.csdn.net/jacke121/article/details/89338898
    # sig_move = pyqtSignal(str)

    def __init__(self, parent=None):
        super(WindowTableProblemsWithMove, self).__init__()

        self.tbl_problems.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tbl_problems.customContextMenuRequested.connect(
            self.custom_right_menu)  # menu 是什么样子的

    # https://blog.csdn.net/MAOZEXIJR/article/details/83111344
    def custom_right_menu(self, pos):
        menu = QMenu()
        data_base = DataBase()
        child_menu = QMenu('move to')

        # addMenu()：在菜单栏上添加一个新的QMenu对象
        # https://www.dazhuanlan.com/2020/03/13/5e6ac5e82cf72/
        # opt_phsics = child_menu.addAction('physics')
        # opt_eng = child_menu.addAction('english')
        opt_new_dir = child_menu.addAction('new dir')
        opt_del_from_fir = child_menu.addAction('del from this dir')
        if not data_base.info:
            print('no info')
            return
        for dir in data_base.info:
            if dir == 'img_ans already':
                continue
            if dir == 'dict_ans':
                continue
            if dir == 'problems':
                continue

            child_menu.addAction(dir)
        menu.addMenu(child_menu)

        action = menu.exec_(self.tbl_problems.mapToGlobal(pos))  # 选择的

        if action == opt_new_dir:
            self.new_dir()

            return

        if action == opt_del_from_fir:
            self.del_from_dir(data_base, action)

            return

        for act in child_menu.actions():

            if act == opt_new_dir or act == opt_del_from_fir:
                continue  # 循环到的act

            if action == act:
                # self.sig_move.emit(act.text())
                problem = self.get_problem()
                if problem == None:
                    print('select nothing')
                    return
                print("problem:")
                print(problem)
                path = act.text()
                dic_ans_path = data_base.info[path]
                dic_ans_path[problem] = data_base.dict_ans[problem]
                # dic_ans 存了所有的答案
                return
        print(pos)

    def del_from_dir(self, data_base, act):
        problem = self.get_problem()
        item = self.tbl_problems.get_item()
        if problem == None:
            print('select nothing')
            return
        # path = act.text()
        path = self.windowTitle()
        print("path:", path)
        dic_ans_path = data_base.info[path]
        dic_ans_path.pop(problem)
        # self.tbl_problems.itemSelectionChanged()
        # print("item.row:",item.row)
        # self.tbl_problems.removeRow(item.row)
        self.tbl_problems._deleteRows()

    def new_dir(self):
        data_base = DataBase()

        # https://blog.csdn.net/rosefun96/article/details/79471674
        path, ok = QInputDialog.getText(
            self, "what is the new dir", "new dir:", QLineEdit.Normal)
        path = path.strip()
        if path == '':
            print('empty can not be a new dir')
            return
        data_base.info[path] = {}
        dic_ans_path = data_base.info[path]
        print('dic_ans_path:')
        print(dic_ans_path)
        problem = self.get_problem()
        dic_ans_path[problem] = data_base.dict_ans[problem]


class TblToListItems(QTableWidget):
    def __init__(self):
        super().__init__()

    def put_items_to_tbl(self, items, not_put: list = None):
        row = 0
        col = 0
        self.setRowCount(len(items))
        self.setColumnCount(1)
        for item in items:
            if not_put and (item in not_put):
                continue
            else:
                self.setItem(row, col, QTableWidgetItem(item))

                row += 1

    def get_item_txt_from_tbl(self):
        item = self.get_item()
        if not item:
            return None
        return item.text()

    def _deleteRows(self):
        # https://blog.csdn.net/weixin_42670810/article/details/104730544
        """
        删除所选择行
        :return:
        """
        print('删除所选择行')
        s_items = self.selectedItems()  # 获取当前所有选择的items
        if s_items:
            selected_rows = []  # 求出所选择的行数
            for i in s_items:
                row = i.row()
                if row not in selected_rows:
                    selected_rows.append(row)
            for r in range(len(sorted(selected_rows))):
                self.removeRow(selected_rows[r]-r)  # 删除行

#         print(len(self.selectedItems()))
# # https://zhuanlan.zhihu.com/p/122462294
#         if len(self.selectedItems())==0:
#             print('select no item')
#             return None
#         row_index = self.currentIndex().row()  # 获取当前行 index
#         if self.item(row_index, 0):
#             item = self.item(row_index, 0).text()  # item(行,列), 获取当前行
#             print("item:")
#             print(item)

#             return item

    def get_item(self):

        # https://zhuanlan.zhihu.com/p/122462294
        if len(self.selectedItems()) == 0:
            print('select no item')
            return None
        row_index = self.currentIndex().row()  # 获取当前行 index
        if self.item(row_index, 0):
            item = self.item(row_index, 0)  # item(行,列), 获取当前行

            return item


# main form
class Form(QWidget):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        font_yahei = QFont("Microsoft YaHei")
        self.setFont(font_yahei)

       
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
        self.txt_msg = QTextEdit()

        # self.window_tbl_problems=WindowListProblems(parent)
        ####

        self.read_txt()

        # self.win_tbl_problems=WindowWithTblProblems()
        self.dir = Direction()

        # self.dir.move(self.win_main.geometry().x() + self.win_main.width() + 10, self.win_main.geometry().y())
        # https://blog.csdn.net/wowocpp/article/details/105221265
        # self.dir.geometry(self.width()+800,self.height(),200,1000)
        # https://blog.csdn.net/caomin1hao/article/details/80388760
        # https://www.cnblogs.com/archisama/p/5444032.html
        # w.move(300, 300)

        # move()方法移动widget组件到一个位置，这个位置是屏幕上x=300,y=300的坐标。

        # setGeometry (9,9, 50, 25) 从屏幕上(9,9)位置开始(即为最左上角的点),显示一个50*25的界面(宽50,高25)
        def set_layout():
            # 设置栅格布局，并添加部件到相应的位置
            layout = QGridLayout()

            
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
           
            layout.addWidget(QPushButton('dir', clicked=self.dir_show))
            layout.addWidget(self.txt_msg)
            # layout.addWidget(self.window_tbl_problems.tbl_problems)
            # 设置主窗口的布局，自定义槽函数，设置标题
            self.setLayout(layout)

        set_layout()

        # connect
        btn_input_ans.clicked.connect(self.input_ans_txt)
        btn_show_ans.clicked.connect(self.show_ans)

        btn_input_ans_img.clicked.connect(self.input_ans_img)
        btn_unshow_ans.clicked.connect(self.unshow_ans)
        btn_save.clicked.connect(self.save)
        btn_modify_ans.clicked.connect(self.modify_ans)

        btn_upgrade_tbl.clicked.connect(self.upgrade_tbl)

        self.setWindowTitle("Learning")

    # https://blog.csdn.net/weixin_45961774/article/details/106008803

    def ans_belongs_to(self, where: str):
        problem = self.window_tbl_problems.get_problem()  # 从tbl获得问题
        data_base = DataBase()
        if where not in data_base.info:
            self.msg('not have this direction, now create')
            data_base.info[where] = {}

        dic_where = data_base.info[where]
        dic_where[problem] = data_base.dict_ans[problem]

    def dir_show(self):
        # https://blog.csdn.net/dengnihuilaiwpl/article/details/90321249
        #         self.dir.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #         self.dir.setFocus()
        # https://blog.csdn.net/Victor_zero/article/details/81268465?utm_source=blogxgwz9
        self.dir.raise_()

        self.dir.show()

    def read_txt(self):
        self.msg('loading..')
        if not os.path.exists('dict_ans.txt'):
            self.msg('not exists,now create')

            init_txt()
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
        data_base = DataBase()

        data_base.info = dic

        data_base.dict_ans = dic['dict_ans']
        cnt_ans_img = dic['img_ans already']
        data_base.cnt_ans_img = cnt_ans_img

        if 'problems' not in dic:

            self.msg('have no problems, please input')
        else:

            data_base.problems = dic['problems']

        file.close()

        self.msg('load done')

    def put_sth_at_table(self, sth, table: QTableWidget):
        table.setItem(0, 0, item=QTableWidgetItem(sth))

    def put_ans_where(self, where: QWidget, problem: str):
        data_base = DataBase()
        if problem not in data_base.dict_ans:
            self.lbl_ans.clear()
            self.msg('have no answer,please give an answer first')
            return
        ans = data_base.dict_ans[problem]

        if 'image/img_ans/' in ans:

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
        data_base = DataBase()
        self.window_tbl_problems.tbl_problems.setRowCount(
            len(data_base.dict_ans) + 1)

        for problem in data_base.dict_ans:

            self.window_tbl_problems.tbl_problems.setItem(
                row, col, QTableWidgetItem(problem))
            row += 1
        print('load done')

    def ans_to_problem(self, problem: str):
        self.put_ans_where(self.lbl_ans, problem=problem)

    def msg(self, msg: str):
        print(msg)
        
        self.txt_msg.append(msg)

    def input_ans_txt(self):
        # https://www.cnblogs.com/ansang/p/7895075.html
        problem = self.txt_input.toPlainText().strip()
        data_base = DataBase()
        if problem in data_base.dict_ans:
            self.msg('already have this problem')
            return
        ans = self.txt_input_ans.toPlainText().strip()
        if ans == '':
            self.msg('没有答案，请输入问题再点击输入')
            return

        data_base.dict_ans[problem] = ans

        self.msg('ans load done')

    def input_ans_img(self):

        self.msg('input a image ans')
        problem = self.txt_input.toPlainText().strip()
        data_base = DataBase()
        if problem in data_base.dict_ans:
            self.msg('already have this problem')
            return
        clipboard = QApplication.clipboard()

        img_ans = clipboard.pixmap()
        if not img_ans:
            self.msg('没有答案，请输入问题再点击输入')
            return
        path = 'image/img_ans/{}.jpg'.format(data_base.cnt_ans_img)
        img_ans.save(path)
        data_base.dict_ans[problem] = path
        data_base.cnt_ans_img += 1
        print('data_base.cnt_ans_img:')
        print(data_base.cnt_ans_img)
        # self.imageLabel.setPixmap(self.dict_ans[problem])

        self.msg('ans load done')

    def show_ans(self):
        # _translate = QtCore.QCoreApplication.translate
        problem = self.txt_input.toPlainText().strip()
        self.ans_to_problem(problem)

    def save(self):

        self.msg('saving..')
        path = './dict_ans.txt'
        file = open(path, 'w')
        data_base = DataBase()
        # dic = {'img_ans already': data_base.cnt_ans_img, 'dict_ans': data_base.dict_ans, 'problems': data_base.problems}

        data_base.info['img_ans already'] = data_base.cnt_ans_img
        file.write(str(data_base.info))
        file.close()

        self.msg('save done')

    def closeEvent(self, event):
        
        self.msg('close')
        self.save()

    def unshow_ans(self):
      
        self.msg('unshow ans')
        self.lbl_ans.clear()

    def modify_ans(self):
        print('messagebox')
        # https://www.cnblogs.com/cxys85/p/10754309.html
        # QMessageBox.addAction('text',action=self.modify_text)
        self.win_choose = Window()  # parent=self.parent
        self.win_choose.resize(500, 200)
        self.win_choose.setWindowTitle('choose type of answer')
        # https://blog.csdn.net/paul200345/article/details/100826879
        self.win_choose.dialogSignel.connect(self.change_param)
        print('win show:')
        self.win_choose.show()

    def change_param(self, choice: str):
        print('change param')
        print('signal:')
        print("choice: ")
        print(choice)
        problem = self.txt_input.toPlainText().strip()
        data_base = DataBase()
        if not problem:
     
            self.msg('没有问题，请输入问题再点击输入')
            return
        if choice == 'text':
            ans = self.txt_input_ans.toPlainText().strip()
            if ans == '':
              
                self.msg('没有问题，请输入问题再点击输入')
                return
            print('ans:')
            print(ans)
            data_base.dict_ans[problem] = ans
        else:
            clipboard = QApplication.clipboard()
            img_ans = clipboard.pixmap()

            if not img_ans:
               
                self.msg('没有问题，请输入问题再点击输入')
                return

            if not problem in data_base.dict_ans:
               
                self.msg('原来没有相应的答案，现在是添加新的答案')
                path = 'image/img_ans/{}.jpg'.format(data_base.cnt_ans_img)
                img_ans.save(path)
                data_base.dict_ans[problem] = path
                data_base.cnt_ans_img += 1
            else:
                path_original = data_base.dict_ans[problem]
                
                self.msg('修改答案')
                img_ans.save(path_original)


# 选择修改text 还是 image
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


class WholeControler():

    def start(self):
        app = QApplication(sys.argv)
        self.win_main = Form()

        self.win_main.show()

        sys.exit(app.exec_())


def init_txt():
    dic = {'img_ans already': 0}
    ans = {}
    
    dic['dict_ans'] = ans
   

    file = open('dict_ans.txt', 'w')
    file.write(str(dic))
    file.close()


whole_controler = WholeControler()
whole_controler.start()
