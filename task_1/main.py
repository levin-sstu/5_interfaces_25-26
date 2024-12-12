import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
from PIL import Image
import os

os.environ['QT_PLUGIN_PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv', 'Lib', 'site-packages',
                                            'PyQt5', 'Qt5', 'plugins')


class PersonFormApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анкета")
        self.initUI()
        self.image_data = None

    def initUI(self):
        self.name_label = QLabel("Имя:")
        self.name_input = QLineEdit()

        self.age_label = QLabel("Возраст:")
        self.age_input = QLineEdit()

        self.bio_label = QLabel("Биография:")
        self.bio_input = QTextEdit()

        self.photo_label = QLabel("Фото:")
        self.photo_preview = QLabel()
        self.photo_preview.setFixedSize(200, 200)
        self.photo_preview.setStyleSheet("border: 1px solid black;")
        self.photo_preview.setAlignment(Qt.AlignCenter)

        self.capture_button = QPushButton("Сделать фото")
        self.capture_button.clicked.connect(self.capture_photo)

        self.save_button = QPushButton("Сохранить анкету")
        self.save_button.clicked.connect(self.save_form)

        self.load_button = QPushButton("Загрузить анкету")
        self.load_button.clicked.connect(self.load_form)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_input)
        layout.addWidget(self.bio_label)
        layout.addWidget(self.bio_input)
        layout.addWidget(self.photo_label)

        photo_layout = QHBoxLayout()
        photo_layout.addWidget(self.photo_preview)
        photo_layout.addWidget(self.capture_button)
        layout.addLayout(photo_layout)

        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def capture_photo(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            QMessageBox.warning(self, "Ошибка", "Не удалось получить доступ к камере.")
            return

        ret, frame = cap.read()
        cap.release()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = rgb_image.shape
            bytes_per_line = 3 * width
            q_image = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio)
            self.photo_preview.setPixmap(scaled_pixmap)

            # Save the image data
            pil_image = Image.fromarray(rgb_image)
            self.image_data = pil_image
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось захватить изображение.")

    def save_form(self):
        name = self.name_input.text()
        age = self.age_input.text()
        bio = self.bio_input.toPlainText()

        if not name or not age or not self.image_data:
            QMessageBox.warning(self, "Ошибка", "Все поля анкеты, включая фото, должны быть заполнены.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить анкету", "", "JSON Files (*.json)")
        if file_path:
            data = {
                "name": name,
                "age": age,
                "bio": bio
            }

            # Save photo as bytes
            photo_path = file_path.replace(".json", "_photo.jpg")
            self.image_data.save(photo_path)

            data["photo_path"] = photo_path

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            QMessageBox.information(self, "Успех", "Анкета успешно сохранена.")

    def load_form(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Загрузить анкету", "", "JSON Files (*.json)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.name_input.setText(data.get("name", ""))
            self.age_input.setText(data.get("age", ""))
            self.bio_input.setText(data.get("bio", ""))

            photo_path = data.get("photo_path", "")
            if photo_path:
                pixmap = QPixmap(photo_path)
                self.photo_preview.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))

            QMessageBox.information(self, "Успех", "Анкета успешно загружена.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PersonFormApp()
    window.show()
    sys.exit(app.exec_())
