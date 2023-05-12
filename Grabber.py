from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import InputPeerEmpty
from MessageProcesser import replace_tags
from NicknameGenerator import generate_nickname
from ToSheetConverter import create_xlsx_with_authors, create_xlsx_tag_nickname


def parse_chats():
    global username, message
    api_id =
    api_hash =
    phone =
    client = TelegramClient(phone, api_id, api_hash, )
    client.start()
    chats = []
    last_date = None
    chunk_size = 200
    groups = []
    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)
    for chat in chats:
        try:
            if chat.megagroup:
                groups.append(chat)
        except:
            continue
    # Скорее всего, для получения всех чатов нужно поменять метод получения всех диалогов с 21 строки
    # https://docs.telethon.dev/en/stable/modules/client.html#telethon.client.dialogs.DialogMethods.iter_dialogs
    # dialogs = await client.get_dialogs()
    # for dialog in dialogs:
    #     print(dialog.title)
    print("Выберите группу для парсинга сообщений и членов группы:")
    i = 0
    for g in groups:
        print(str(i) + "- " + g.title)
        i += 1
    g_index = input("Введите нужную цифру: ")
    target_group = groups[int(g_index)]
    print("Узнаём пользователей...")
    all_participants = client.get_participants(target_group)
    participants_fake_names = {}
    print("Сохраняем данные в файл...")
    for user in all_participants:
        if user.username:
            username = user.username
        else:
            username = ""
        if username in participants_fake_names:
            pass
        else:
            participants_fake_names[username] = generate_nickname()
    print(participants_fake_names)
    create_xlsx_tag_nickname(participants_fake_names)
    print("Парсинг участников группы успешно выполнен.")
    offset_id = 0
    limit = 100
    all_messages = []
    authors = []
    total_messages = 0
    total_count_limit = 0
    messages_dict = {}
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
        if not history.messages:
            break
        messages = history.messages

        i = 0
        for message in messages:
            if message.from_id is None:
                break
            else:
                author_id = message.from_id.user_id
                author = client.get_entity(author_id)
                author_username = author.username
                sending_date = message.date
                text = replace_tags(message.message, participants_fake_names)
            messages_dict[i] = {
                'Дата отправки': sending_date,
                'Имя отправителя': participants_fake_names[author_username],
                'Сообщение': text,
                'В ответ на': message.reply_to
            }

        offset_id = messages[len(messages) - 1].id
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break
    print("Сохраняем данные в файл...")
    create_xlsx_with_authors(messages_dict)
    print('Парсинг сообщений группы успешно выполнен.')
