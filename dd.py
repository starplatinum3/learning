import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel, QFileDialog, QTableWidget, QTableWidgetItem, QLineEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.path_input = QLineEdit("D:")
        self.button_change_path = QPushButton("切换路径")
        self.button_list = QPushButton("列出文件夹")
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["文件名", "大小", "创建时间", "修改时间"])

        self.button_change_path.clicked.connect(self.change_folder_path)
        self.button_list.clicked.connect(self.list_folder_contents)

        layout = QVBoxLayout()
        layout.addWidget(self.path_input)
        layout.addWidget(self.button_change_path)
        layout.addWidget(self.button_list)
        layout.addWidget(self.table_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def change_folder_path(self):
        new_folder_path = self.path_input.text()
        if os.path.isdir(new_folder_path):
            self.current_folder_path = new_folder_path

    def list_folder_contents(self):
        folder_path = self.current_folder_path
        contents = os.listdir(folder_path)
        self.table_widget.setRowCount(len(contents))
        for row, item_name in enumerate(contents):
            file_path = os.path.join(folder_path, item_name)
            file_info = os.stat(file_path)
            self.table_widget.setItem(row, 0, QTableWidgetItem(item_name))
            self.table_widget.setItem(row, 1, QTableWidgetItem(str(file_info.st_size)))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(file_info.st_ctime)))
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(file_info.st_mtime)))


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

# D:\proj\python\learning>python "d:\proj\python\learning\dd.py"
# Traceback (most recent call last):
#   File "d:\proj\python\learning\dd.py", line 34, in list_folder_contents
#     folder_path = self.current_folder_path
# AttributeError: 'MainWindow' object has no attribute 'current_folder_path'