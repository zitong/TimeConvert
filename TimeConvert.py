import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QDesktopWidget
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QDateTime, Qt, QTimer
import re

class TimeConverterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):

        # 创建一个文本控件显示当前时间

        self.current_time_label = QLabel(self)
        self.current_timestamp_label = QLabel(self)

        copy_time_button = QPushButton('拷贝时间', self)
        copy_time_button.clicked.connect(self.copy_time)

        copy_timestamp_button = QPushButton('拷贝时间戳', self)
        copy_timestamp_button.clicked.connect(self.copy_timestamp)


        self.text_input = QTextEdit(self)
        self.text_output = QTextEdit(self)

        convert_to_time_button = QPushButton('转换为时间', self)
        convert_to_time_button.clicked.connect(self.convert_to_time)

        convert_to_timestamp_button = QPushButton('转换为时间戳', self)
        convert_to_timestamp_button.clicked.connect(self.convert_to_timestamp)

        
        hbox_top = QHBoxLayout()
        hbox_top.addWidget(self.current_time_label)
        hbox_top.addWidget(self.current_timestamp_label)

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(copy_time_button)
        hbox_buttons.addWidget(copy_timestamp_button)

        hbox = QHBoxLayout()
        hbox.addWidget(self.text_input)
        hbox.addWidget(self.text_output)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_top)
        vbox.addLayout(hbox_buttons)
        vbox.addLayout(hbox)
        vbox.addWidget(convert_to_time_button)
        vbox.addWidget(convert_to_timestamp_button)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 800, 800)
         # 获取屏幕的宽度和高度
        screen = QDesktopWidget().screenGeometry()
        screen_width, screen_height = screen.width(), screen.height()

        # 计算窗口初始位置
        x = (screen_width - self.width()) // 2
        y = (screen_height - self.height()) // 2

        self.move(x, y)  # 设置窗口初始位置

        self.setWindowTitle('时间戳转换工具')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_current_time)
        self.timer.start(1000)  # 更新间隔为1秒
        self.update_current_time()

        self.show()

    def convert_to_time(self):
        input_text = self.text_input.toPlainText()
        output_text = re.sub(r'\d+', lambda match: self.timestamp_to_time(match.group()), input_text)
        self.text_output.setPlainText(output_text)

    def convert_to_timestamp(self):
        input_text = self.text_output.toPlainText()
        output_text = re.sub(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', lambda match: self.time_to_timestamp(match.group()), input_text)
        self.text_input.setPlainText(output_text)

    def timestamp_to_time(self, timestamp_str):
        try:
            timestamp = int(timestamp_str)
            if timestamp < 999999:
                return timestamp_str
            dt = QDateTime.fromSecsSinceEpoch(timestamp)
            return dt.toString('yyyy-MM-dd hh:mm:ss')
        except ValueError:
            return timestamp_str

    def time_to_timestamp(self, time_str):
        try:
            dt = QDateTime.fromString(time_str, 'yyyy-MM-dd hh:mm:ss')
            timestamp = dt.toSecsSinceEpoch()
            return str(timestamp)
        except ValueError:
            return time_str
    def update_current_time(self):
        current_time = QDateTime.currentDateTime()
        current_timestamp = current_time.toSecsSinceEpoch()

        self.current_time_label.setText(f'当前时间: {current_time.toString("yyyy-MM-dd hh:mm:ss")}')
        self.current_timestamp_label.setText(f'当前时间戳: {current_timestamp}')

    def copy_timestamp(self):
        current_timestamp = QDateTime.currentDateTime().toSecsSinceEpoch()
        clipboard = QApplication.clipboard()
        clipboard.setText(str(current_timestamp))

    def copy_time(self):
        current_time = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
        clipboard = QApplication.clipboard()
        clipboard.setText(current_time)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TimeConverterApp()
    sys.exit(app.exec_())
