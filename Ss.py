import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, \
    QWidget, QPushButton, QTextEdit, QLabel, QFileDialog, QListWidget, QListWidgetItem\
    ,QSizePolicy

class FileItemWidget(QWidget):
    # def __init__(self, file_name, file_info):
    #     super(FileItemWidget, self).__init__()

    #     self.name_label = QLabel(file_name)

    #     info_str = f"文件名: {file_name}\n"
    #     info_str += f"大小: {file_info.st_size} bytes\n"
    #     info_str += f"创建时间: {file_info.st_ctime}\n"
    #     info_str += f"修改时间: {file_info.st_mtime}"
    #     self.info_label = QLabel(info_str)

    #     layout = QVBoxLayout()
    #     layout.addWidget(self.name_label)
    #     layout.addWidget(self.info_label)
    #     self.setLayout(layout)
    def __init__(self, file_name, file_info):
        super(FileItemWidget, self).__init__()

        self.name_label = QLabel(file_name)
        self.name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        info_str = f"文件名: {file_name}\n"
        info_str += f"大小: {file_info.st_size} bytes\n"
        info_str += f"创建时间: {file_info.st_ctime}\n"
        info_str += f"修改时间: {file_info.st_mtime}"
        print("info_str")
        print(info_str)
        self.info_label = QLabel(info_str)
        self.info_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.info_label)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.button_list = QPushButton("列出文件夹")
        self.text_edit = QTextEdit()
        self.file_list = QListWidget()

        self.button_list.clicked.connect(self.list_folder_contents)

        layout = QVBoxLayout()
        layout.addWidget(self.button_list)
        layout.addWidget(self.file_list)
        layout.addWidget(self.text_edit)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def list_folder_contents(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            contents = os.listdir(folder_path)
            self.file_list.clear()
            for item_name in contents:
                file_path = os.path.join(folder_path, item_name)
                file_info = os.stat(file_path)
                item_widget = FileItemWidget(item_name, file_info)
                item = QListWidgetItem(self.file_list)
                self.file_list.addItem(item)
                self.file_list.setItemWidget(item, item_widget)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
