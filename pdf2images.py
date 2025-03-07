import cv2
import numpy as np
import easyocr
import fitz
import os
import pytesseract

from rotator import image_rotator

def pdf_to_images(pdf_path, output_folder):
    # Открываем PDF файл
    pdf_document = fitz.open(pdf_path)

    # Создаем папку для сохранения изображений, если она не существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Проходим по всем страницам PDF
    for page_number in range(len(pdf_document)):
        # Получаем страницу
        page = pdf_document.load_page(page_number)

        # Преобразуем страницу в изображение (PNG)
        pix = page.get_pixmap()

        # Преобразуем Pixmap в массив NumPy
        image = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)

        # Увеличиваем изображение в 3 раза
        (height, width) = image.shape[:2]
        height, width = int(height * 3), int(width * 3)
        image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)

        # Если изображение в формате RGBA, преобразуем его в RGB
        if pix.n == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Автоматический поворот изображения
        rotated_image = image_rotator(image)

        # Сохраняем изображение в папку
        image_path = os.path.join(output_folder, f"page_{page_number + 1}.png")
        cv2.imwrite(image_path, rotated_image)

    # Закрываем PDF файл
    pdf_document.close()

# Пример использования
pdf_to_images("test.pdf", "img")

