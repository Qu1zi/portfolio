import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QTextEdit, QListWidget, QHBoxLayout, QMessageBox, QLabel, QGroupBox
from database import Database

class DetailApp(QMainWindow):
    def __init__(self, database):
        super().__init__()

        self.database = database

        self.setWindowTitle("Управление деталями")
        self.setGeometry(100, 100, 800, 500)

        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout()

        # Левая часть окна с списком деталей
        self.left_panel = QGroupBox("Детали")
        self.left_layout = QVBoxLayout()

        self.detail_list = QListWidget()
        self.detail_list.itemClicked.connect(self.show_detail)

        self.load_details()

        self.left_layout.addWidget(self.detail_list)
        self.left_panel.setLayout(self.left_layout)

        # Правая часть окна с информацией о детали
        self.right_panel = QGroupBox("Информация о детали")
        self.right_layout = QVBoxLayout()

        self.detail_info = QTextEdit()
        self.detail_info.setReadOnly(True)

        self.right_layout.addWidget(self.detail_info)
        self.right_panel.setLayout(self.right_layout)

        # Форма для добавления детали
        self.form_panel = QGroupBox("Добавить деталь")
        self.form_layout = QVBoxLayout()

        self.detail_input = QLineEdit()
        self.detail_input.setPlaceholderText("Название детали")

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Описание")

        add_button = QPushButton("Добавить")
        add_button.clicked.connect(self.add_detail)

        delete_button = QPushButton("Удалить")
        delete_button.clicked.connect(self.delete_detail)

        self.form_layout.addWidget(self.detail_input)
        self.form_layout.addWidget(self.description_input)
        self.form_layout.addWidget(add_button)
        self.form_layout.addWidget(delete_button)

        self.form_panel.setLayout(self.form_layout)

        # Добавляем все элементы на главное окно
        self.layout.addWidget(self.left_panel)
        self.layout.addWidget(self.right_panel)
        self.layout.addWidget(self.form_panel)

        self.central_widget.setLayout(self.layout)

    def add_detail(self):
        name = self.detail_input.text()
        description = self.description_input.toPlainText()
        if name:
            self.database.add_detail(name, description)
            self.detail_input.clear()
            self.description_input.clear()
            self.load_details()
        else:
            QMessageBox.critical(self, 'Ошибка', 'Пожалуйста, введите название детали')

    def delete_detail(self):
        selected_item = self.detail_list.currentItem()
        if selected_item:
            detail_id = int(selected_item.text().split(":")[0])
            self.database.delete_detail(detail_id)
            self.load_details()
            self.detail_info.clear()
        else:
            QMessageBox.warning(self, 'Предупреждение', 'Выберите деталь для удаления')

    def load_details(self):
        self.detail_list.clear()
        details = self.database.get_details()
        for detail in details:
            item = f"{detail[0]}: {detail[1]}"
            self.detail_list.addItem(item)

    def show_detail(self, item):
        detail_id = int(item.text().split(":")[0])
        detail = self.database.get_detail(detail_id)
        if detail:
            self.detail_info.setPlainText(f"Название: {detail[0]}\n\nОписание: {detail[1]}")

    def closeEvent(self, event):
        self.database.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    database = Database()
    window = DetailApp(database)
    window.show()
    sys.exit(app.exec_())
