import os
import xlsxwriter


def get_path_to_xlsx(sheet_name):
    path = os.getcwd() + '\\' + sheet_name
    return path


def create_xlsx_with_authors(messages, sheet_name='chat_history_with_authors.xlsx'):
    workbook = xlsxwriter.Workbook(sheet_name)
    worksheet = workbook.add_worksheet()
    row = 0
    author_col = 0
    message_col = 1

    worksheet.write(row, author_col, 'Автор')
    worksheet.write(row, message_col, 'Сообщение')

    for author, message in messages:
        row += 1
        worksheet.write(row, author_col, author)
        worksheet.write(row, message_col, message)

    workbook.close()
    return get_path_to_xlsx(sheet_name)


def create_xlsx_without_authors(messages, sheet_name='chat_history_without_authors.xlsx'):
    workbook = xlsxwriter.Workbook(sheet_name)
    worksheet = workbook.add_worksheet()
    row = 0
    message_col = 0

    worksheet.write(row, message_col, 'Сообщение')

    for author, message in messages:
        row += 1
        worksheet.write(row, message_col, message)

    workbook.close()
    return get_path_to_xlsx(sheet_name)
