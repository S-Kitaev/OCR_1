import cv2
import pytesseract
from pytesseract import Output, TesseractError
from datetime import datetime

start = datetime.now()

def image_rotator(image):
	# Настройка пути к Tesseract
	pytesseract.pytesseract.tesseract_cmd = r'tesseract\tesseract.exe'
	pytesseract.pytesseract.tessdata_dir_config = r'--tessdata-dir "tesseract\tessdata"'

	# Преобразуем изображение в RGB
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	try:
		results = pytesseract.image_to_osd(rgb, output_type=Output.DICT)
	except TesseractError as e:
		print(f"Ошибка обработки изображения: {e}")
		return image  # Возвращаем исходное изображение без поворота

	rotate_counter = 0
	# Если текст не кириллица, поворачиваем изображение
	if results["script"] != "Cyrillic":
		while results["script"] != "Cyrillic" and rotate_counter < 4:
			image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
			rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Обновляем изображение
			try:
				results = pytesseract.image_to_osd(rgb, output_type=Output.DICT)
			except TesseractError as e:
				print(f"Ошибка обработки изображения при повороте: {e}")
				break  # Прекращаем попытки поворота
			rotate_counter += 1

	return image
	# cv2.imwrite(image_path, image)
	# lang_group = results["script"]
	# angle = rotate_counter * 90

	# end = datetime.now()

	# Вывод информации о результате
	print(f"Изображение {image_path} было повернуто на {angle} градусов")
	print(f"Распознаны {lang_group} символы, затраченное время {end - start}")

# image_rotator("img/page_3.png")
