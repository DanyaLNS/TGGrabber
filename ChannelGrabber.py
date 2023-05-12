from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import InputPeerEmpty

from MessageProcesser import replace_tags
from NicknameGenerator import generate_nickname
from ToSheetConverter import create_xlsx_with_authors, create_xlsx_tag_nickname


def parse_channels():
    global username, message
    # Креды
    api_id =
    api_hash =
    phone =
    # Установка соединения с тг апи
    client = TelegramClient(phone, api_id, api_hash, )
    client.start()
    # Переменные для получения
    chats = []
    last_date = None
    chunk_size = 200
    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    # Сохраняем вообще все полученные чаты
    chats.extend(result.chats)
    # Условие было для проверки, можно ли парсить чат/канал тг
    # Канал можно парсить, только если он принадлежит тебе или в нём больше 200 подписчиков
    # for chat in chats:
    #     try:
    #         if chat.megagroup:
    #             groups.append(chat)
    #     except:
    #         continue
    print("Выберите группу для парсинга сообщений и членов группы:")
    i = 0
    for chat in chats:
        print(str(i) + "- " + chat.title)
        i += 1
    g_index = input("Введите нужную цифру: ")
    target_group = chats[int(g_index)]
    print("Сохраняем сообщения...")

    # Переменные для парсинга сообщений
    participants_fake_names = {}
    offset_id = 0
    limit = 100
    authors = []
    total_messages = 0
    total_count_limit = 0
    messages_dict = []
    # Считываем по 100 сообщений за раз
    while True:
        history = client(GetHistoryRequest(
            peer=target_group,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        # Если сообщения закончились, прерываем циклы
        if not history.messages:
            break
        # Если нет, обрабатываем сообщения
        messages = history.messages

        i = 0
        # В каждом сообщении заменяем имя отправителя, удаляем тэги из текста
        for message in messages:
            # Без этого условия всё валится на последнем сообщении
            if message.from_id is None:
                break
            else:
                # Получаем тэг автора сообщения
                author_id = message.from_id.user_id
                author = client.get_entity(author_id)
                author_username = author.username
                # Находим его в списке имеющихся фейковых имен или присваиваем новое
                if author_username in authors:
                    fake_name = participants_fake_names[author_username]
                else:
                    fake_name = generate_nickname()
                    participants_fake_names[author_username] = fake_name
                # Устанавливаем дату отправки
                sending_date = message.date
                # Устанавливаем текст без тэгов
                text = replace_tags(message.message, participants_fake_names)
                # Сохраняем запись сообщения в словарь словарей
                messages_dict[i] = {
                    'Дата отправки': sending_date,
                    'Имя отправителя': fake_name,
                    'Сообщение': text,
                    'В ответ на': message.reply_to
                }
        # Установка, с какого сообщения нужно продолжать парсинг
        offset_id = messages[len(messages) - 1].id
        # Еще одно условие выхода
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break
    # Создание таблиц
    print("Сохраняем данные в файл...")
    create_xlsx_tag_nickname(participants_fake_names)
    create_xlsx_with_authors(messages_dict)
    print('Парсинг сообщений группы успешно выполнен.')
