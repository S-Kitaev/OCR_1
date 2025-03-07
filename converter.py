from PIL import Image
import pytesseract
from pdf2images import pdf_to_images
import os

text_from_images = []

def image_to_text(image_path, langs="rus+eng"):
    # Считываем изображение
    img = Image.open(image_path)
    # Путь к тессеракту
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Huawei\Desktop\PDFNN\tesseract\tesseract.exe'
    # Извлекаем текст из изображения
    text = pytesseract.image_to_string(img, lang=langs)
    return text

def process_images():
    folder = 'img'
    output_file = 'text.txt'

    # Проверяем, существует ли папка
    if not os.path.exists(folder):
        print(f'Папка {folder} не найдена!')
        return

    # Получаем список файлов в папке
    files = os.listdir(folder)

    with open(output_file, 'w', encoding='utf-8') as f:
        for file in range(len(files)):
            file_path = os.path.join(folder, files[file])

            if os.path.isfile(file_path):
                result = image_to_text(f"img/page_{file + 1}.png")
                f.write(result)


pdf_to_images("test.pdf")
process_images()
