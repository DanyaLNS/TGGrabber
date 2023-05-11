def replace_tags(message, fake_names):
    for tag, nickname in fake_names.items():
        if message.find(tag):
            message = message.replace(tag, nickname)
    return message
