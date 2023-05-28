import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel, QFileDialog, QListWidget, QListWidgetItem

class FileItemWidget(QWidget):
    def __init__(self, file_name, file_info):
        super(FileItemWidget, self).__init__()

        # 创建标签用于显示文件名
        self.name_label = QLabel(file_name)

        # 创建标签用于显示文件信息
        info_str = f"文件名: {file_name}\n"
        info_str += f"大小: {file_info.st_size} bytes\n"
        info_str += f"创建时间: {file_info.st_ctime}\n"
        info_str += f"修改时间: {file_info.st_mtime}"
        self.info_label = QLabel(info_str)

        # 创建垂直布局，并将标签添加到布局中
        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.info_label)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 创建按钮、文本框和文件列表
        self.button_list = QPushButton("列出文件夹")
        self.text_edit = QTextEdit()
        self.file_list = QListWidget()

        # 将按钮点击事件连接到自定义的槽函数
        self.button_list.clicked.connect(self.list_folder_contents)

        # 创建主布局
        layout = QVBoxLayout()
        layout.addWidget(self.button_list)
        layout.addWidget(self.file_list)
        layout.addWidget(self.text_edit)

        # 创建主窗口部件并将布局设置为主窗口的布局
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def list_folder_contents(self):
        # 打开文件夹选择对话框
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            # 获取文件夹中的文件和文件夹列表
            contents = os.listdir(folder_path)
            # 清空文件列表
            self.file_list.clear()
            # 将文件列表项添加到文件列表中
            for item_name in contents:
                # 构建文件路径
                file_path = os.path.join(folder_path, item_name)
                # 获取文件信息
                file_info = os.stat(file_path)
                # 创建自定义的文件项
                item_widget = FileItemWidget(item_name, file_info)
                # 将自定义的文件项添加到文件列表中
                item = QListWidgetItem(self.file_list)
                self.file_list.setItemWidget(item, item_widget)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
