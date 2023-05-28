import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel, QFileDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 创建按钮、文本框和标签
        self.button_list = QPushButton("列出文件夹")
        self.button_view = QPushButton("查看文件信息")
        self.text_edit = QTextEdit()
        self.file_label = QLabel()

        # 将按钮点击事件连接到自定义的槽函数
        self.button_list.clicked.connect(self.list_folder_contents)
        self.button_view.clicked.connect(self.view_file_info)

        # 创建主布局
        layout = QVBoxLayout()
        layout.addWidget(self.button_list)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.button_view)
        layout.addWidget(self.file_label)

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
            # 将列表转换为字符串并显示在文本框中
            self.text_edit.setText('\n'.join(contents))

    def view_file_info(self):
        # 打开文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if file_path:
            # 获取文件信息
            file_info = os.stat(file_path)
            # 构建文件信息字符串
            info_str = f"文件名: {os.path.basename(file_path)}\n"
            info_str += f"大小: {file_info.st_size} bytes\n"
            info_str += f"创建时间: {file_info.st_ctime}\n"
            info_str += f"修改时间: {file_info.st_mtime}"
            # 在标签中显示文件信息
            self.file_label.setText(info_str)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
