import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 创建按钮和文本框
        self.button = QPushButton("列出文件夹")
        self.text_edit = QTextEdit()

        # 将按钮点击事件连接到自定义的槽函数
        self.button.clicked.connect(self.list_folder_contents)

        # 创建主布局
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.text_edit)

        # 创建主窗口部件并将布局设置为主窗口的布局
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def list_folder_contents(self):
        # 获取当前文件夹路径
        current_folder = os.getcwd()

        # 获取当前文件夹中的文件和文件夹列表
        contents = os.listdir(current_folder)

        # 将列表转换为字符串并显示在文本框中
        self.text_edit.setText('\n'.join(contents))


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
