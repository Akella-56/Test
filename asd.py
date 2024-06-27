import PyPDF2

def convert_txt_to_pdf(input_txt_file, output_pdf_file):
    # Открываем текстовый файл для чтения
    with open(input_txt_file, 'r', encoding='utf-8') as txt_file:
        text_content = txt_file.read()

    # Создаем объект для записи PDF
    pdf_writer = PyPDF2.PdfWriter()

    # Создаем новую страницу PDF
    page = pdf_writer.add_page(width=595.32, height=841.92)  # A4 размер (в точках)

    # Создаем объект текста на странице
    page.add_text(text_content)

    # Записываем PDF в файл
    with open(output_pdf_file, 'wb') as pdf_file:
        pdf_writer.write(pdf_file)

if __name__ == '__main__':
    output_txt_path = r"C:\Users\danil\Documents\deploy\output.txt"
    output_pdf_path = r"C:\Users\danil\Documents\deploy\output.pdf"

    convert_txt_to_pdf(output_txt_path, output_pdf_path)
    print(f'PDF файл успешно создан: {output_pdf_path}')
