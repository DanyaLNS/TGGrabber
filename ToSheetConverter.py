import os

import xlsxwriter


def get_path_to_xlsx(sheet_name):
    path = os.getcwd() + '\\' + sheet_name
    return path


def create_xlsx_tag_nickname(tag_nickname_dict, sheet_name='tag_nickname.xlsx'):
    workbook = xlsxwriter.Workbook(sheet_name)
    worksheet = workbook.add_worksheet()
    row = 0
    tag_col = 0
    nickname_col = 1

    worksheet.write(row, tag_col, 'Тэг')
    worksheet.write(row, nickname_col, 'Никнейм')

    for tag, nickname in tag_nickname_dict.items():
        row += 1
        worksheet.write(row, tag_col, tag)
        worksheet.write(row, nickname_col, nickname)

    workbook.close()
    return get_path_to_xlsx(sheet_name)


def create_xlsx_with_authors(messages_dict, sheet_name='chat_history_with_authors.xlsx'):
    workbook = xlsxwriter.Workbook(sheet_name, {'remove_timezone': True})
    worksheet = workbook.add_worksheet()
    row = 0
    date_col = 0
    author_col = 1
    message_col = 2
    reply_col = 3

    worksheet.write(row, date_col, 'Дата отправки')
    worksheet.write(row, author_col, 'Автор')
    worksheet.write(row, message_col, 'Сообщение')
    worksheet.write(row, reply_col, 'В ответ на')

    for key, message in messages_dict.items():
        row += 1
        worksheet.write(row, date_col, message['Дата отправки'])
        worksheet.write(row, author_col, message['Имя отправителя'])
        worksheet.write(row, date_col, message['Сообщение'])
        worksheet.write(row, reply_col, message['В ответ на'])

    workbook.close()
    return get_path_to_xlsx(sheet_name)
