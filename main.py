import re
import base64
# Пися кака


# Функция находит первый и последний байт PDF документа из form-data
def pdf_search(byte_values):
    # Ищем начало PDF
    startPDF = None
    for i in range(len(byte_values)):
        if byte_values[i:i + 4] == [37, 80, 68, 70]:  # Сигнатура PDF: %PDF
            startPDF = i
            break

    if startPDF is None:
        raise ValueError('Не удалось найти начало PDF')

    # Ищем конец PDF
    endPDF = None
    for i in range(len(byte_values) - 1, startPDF, -1):
        if byte_values[i - 4:i + 1] == [37, 37, 69, 79, 70]:  # Сигнатура конца PDF: %%EOF
            endPDF = i + 1
            break

    if endPDF is None:
        raise ValueError('Не удалось найти конец PDF')

    return startPDF, endPDF

def save_pdf(byte_values, startPDF, endPDF, output_file):
    # Извлекаем байты PDF
    pdf_bytes = byte_values[startPDF:endPDF]
    byte_array = bytearray(pdf_bytes)
    print("1111111111")
    # Сохраняем байтовый объект как PDF файл
    with open(output_file, 'wb') as f:
        f.write(byte_array)
    print("22222222222")

def read_form_data_from_file(file_path):
    with open(txt_file_path, 'r') as f:
        content = f.read()

    # Исключаем первый и последний символ
    trimmed_content = content[1:-1]

    # Разбиваем строку на отдельные значения байтовых объектов
    byte_values = [int(value.strip()) for value in trimmed_content.split(',')]

    startPDF, endPDF = pdf_search(byte_values)

    # Сохраняем PDF как файл
    output_pdf_file = r"C:\Users\danil\Documents\deploy\extracted_pdf.pdf"
    save_pdf(byte_values, startPDF, endPDF, output_pdf_file)

    # Преобразуем список целых чисел в байтовый объект
    byte_array = bytes(byte_values)

    # Декодируем байтовый объект в строку с использованием кодировки ISO-8859-1 (Latin-1)
    decoded_string = byte_array.decode('utf-8')

    # Находим content-type и извлекаем границу
    match_content_type = re.search(b'Content-Type: multipart/form-data; boundary=(.*)', content)
    if not match_content_type:
        raise ValueError('Не удалось найти boundary в файле')

    boundary = match_content_type.group(1).strip()

    # Разделяем содержимое файла на части, используя boundary
    parts = re.split(r'--' + re.escape(boundary), content)
    form_data = {}

    # Проходим по частям и извлекаем значения параметров
    for part in parts:
        if not part.strip():
            continue

        # Ищем параметр document_id_1c
        match_doc_id = re.search(r'name="document_id_1c"\s*\r\n\r\n(.*)\r\n', part, re.DOTALL)
        if match_doc_id:
            form_data['document_id_1c'] = match_doc_id.group(1).strip()

        # Ищем параметр file
        match_file = re.search(r'name="file"; filename="(.*)"\r\nContent-Type: (.*)\r\n\r\n(.*)\r\n', part, re.DOTALL)
        if match_file:
            file_name = match_file.group(1)
            content_type = match_file.group(2)
            file_content_base64 = match_file.group(3)

            form_data['file_name'] = file_name
            form_data['content_type'] = content_type
            form_data['file_content'] = file_content_base64

    return form_data


# Пример использования
if __name__ == "__main__":
    txt_file_path = r"C:\Users\danil\Documents\deploy\output.txt"
    form_data = read_form_data_from_file(txt_file_path)

    # Выводим извлеченные данные
    print(f"document_id_1c: {form_data.get('document_id_1c')}")
    print(f"file_name: {form_data.get('file_name')}")
    print(f"content_type: {form_data.get('content_type')}")
    # Предполагая, что содержимое файла file является base64
    print(f"file_content (first 100 bytes): {form_data.get('file_content')[:100]}")

#
# # Строка с байтовыми значениями и текстом
# byte_string = "45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 55, 57, 48, 50, 48, 55, 50, 49, 56, 51, 54, 52, 52, 52, 53, 57, 49, 53, 51, 54, 55, 55, 50, 55, 13, 10, 67, 111, 110, 116, 101, 110, 116, 45, 68, 105, 115, 112, 111, 115, 105, 116, 105, 111, 110, 58, 32, 102, 111, 114, 109, 45, 100, 97, 116, 97, 59, 32, 110, 97, 109, 101, 61, 34, 100, 111, 99, 117, 109, 101, 110, 116, 95, 105, 100, 95, 49, 99, 34, 13, 10, 13, 10, 54, 102, 55, 52, 101, 56, 56, 57, 45, 48, 98, 51, 49, 45, 49, 49, 101, 102, 57, 56, 52, 56, 45, 51, 99, 101, 99, 101, 102, 48, 102, 54, 102, 101, 100, 13, 10"
#
# # Разбиваем строку на отдельные значения
# byte_values = [int(value.strip()) for value in byte_string.split(',')]
#
# # Преобразуем список целых чисел в байтовый объект
# byte_array = bytes(byte_values)
#
# # Декодируем байтовый объект в строку с использованием кодировки UTF-8
# decoded_string = byte_array.decode('utf-8')
#
# # Вывод результата
# print(f"Исходная строка: {byte_string}")
# print(f"Декодированная строка: {decoded_string}")
