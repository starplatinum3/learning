import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel, QFileDialog, QTableWidget, QTableWidgetItem, QListWidget, QListWidgetItem

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.path_input = QTextEdit("D:")
        self.path_input.setMaximumHeight(30)  # 设置输入框高度
        self.button_change_path = QPushButton("切换路径")
        self.button_parent_path = QPushButton("上一级目录")
        self.button_list = QPushButton("列出文件夹")
        self.file_list = QListWidget()

        self.button_change_path.clicked.connect(self.change_folder_path)
        self.button_parent_path.clicked.connect(self.go_up_folder)
        self.button_list.clicked.connect(self.list_folder_contents)
        self.file_list.itemDoubleClicked.connect(self.enter_folder)

        layout = QVBoxLayout()
        layout.addWidget(self.path_input)
        layout.addWidget(self.button_change_path)
        layout.addWidget(self.button_parent_path)
        layout.addWidget(self.button_list)
        layout.addWidget(self.file_list)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def change_folder_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            self.path_input.setText(folder_path)

    def go_up_folder(self):
        current_path = self.path_input.toPlainText()
        parent_path = os.path.dirname(current_path)
        if os.path.isdir(parent_path):
            self.path_input.setText(parent_path)
            self.list_folder_contents()  # 切换到上一级目录后自动列出文件夹中的文件

    def list_folder_contents(self):
        folder_path = self.path_input.toPlainText()
        if os.path.isdir(folder_path):
            self.file_list.clear()
            contents = os.listdir(folder_path)
            for item_name in contents:
                item = QListWidgetItem(item_name)
                # 设置文件夹路径作为附加数据
                file_path = os.path.join(folder_path, item_name)
                item.setData(0, file_path)
                self.file_list.addItem(item)

    def enter_folder(self, item):
        file_path = item.data(0)
        if os.path.isdir(file_path):
            self.path_input.setText(file_path)
            self.list_folder_contents()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
