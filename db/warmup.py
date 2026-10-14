



messages = [
    "1. «Я еду на TechHeads 2026»",
    "2. «Обсуждаем #techheads сегодня»",
    "3. «Смотрю доклады о Python»",
    "4. «Отзывы о TECHHEADS отличные»",
    "5. «Завтра встреча команды»"
]
keyword = "techheads"

def find_mentions(messages, keyword):
        
    return [message for message in messages if keyword.lower() in message.lower()]

print(find_mentions(messages, keyword))