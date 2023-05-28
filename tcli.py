import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel, QFileDialog, QTableWidget, QTableWidgetItem

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.path_input = QTextEdit("D:/")
        self.path_input.setMaximumHeight(30)  # 设置输入框高度
        self.button_change_path = QPushButton("切换路径")
        self.button_parent_path = QPushButton("上一级目录")
        self.button_list = QPushButton("列出文件夹")
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["文件名", "大小", "创建时间", "修改时间", "类型"])

        self.button_change_path.clicked.connect(self.change_folder_path)
        self.button_parent_path.clicked.connect(self.go_up_folder)
        self.button_list.clicked.connect(self.list_folder_contents)
        self.table_widget.itemDoubleClicked.connect(self.open_folder)

        layout = QVBoxLayout()
        layout.addWidget(self.path_input)
        layout.addWidget(self.button_change_path)
        layout.addWidget(self.button_parent_path)
        layout.addWidget(self.button_list)
        layout.addWidget(self.table_widget)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def change_folder_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            self.path_input.setText(folder_path)

    # def go_up_folder(self):
    #     current_path = self.path_input.toPlainText()
    #     parent_path = os.path.dirname(current_path)
    #     if os.path.isdir(parent_path):
    #         self.path_input.setText(parent_path)
    def go_up_folder(self):
        current_path = self.path_input.toPlainText()
        parent_path = os.path.dirname(current_path)
        if os.path.isdir(parent_path):
            self.path_input.setText(parent_path)
            self.list_folder_contents()  # 切换到上一级目录后自动列出文件夹中的文件


    def list_folder_contents(self):
        folder_path = self.path_input.toPlainText()
        if os.path.isdir(folder_path):
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)
            contents = os.listdir(folder_path)
            for item_name in contents:
                item_path = os.path.join(folder_path, item_name)
                item_info = os.stat(item_path)
                item_size = item_info.st_size
                item_ctime = item_info.st_ctime
                item_mtime = item_info.st_mtime
                item_type = "文件夹" if os.path.isdir(item_path) else "文件"
                self.add_table_row(item_name, item_size, item_ctime, item_mtime, item_type)

    def add_table_row(self, name, size, ctime, mtime, item_type):
        row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(row_count)
        self.table_widget.setItem(row_count, 0, QTableWidgetItem(name))
        self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(size)))
        self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(ctime)))
        self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(mtime)))
        self.table_widget.setItem(row_count, 4, QTableWidgetItem(item_type))

    def open_folder(self, item):
        column = item.column()
        if column == 0:  # 文件名列
            file_name = item.text()
            folder_path = self.path_input.toPlainText()
            file_path = os.path.join(folder_path, file_name)
            if os.path.isdir(file_path):
                self.path_input.setText(file_path)
                self.list_folder_contents()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
