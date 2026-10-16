



messages = [
    "Были на TechHeads, очень понравилось!",
    "techheads — лучший доклад про AI",
    "Кто идёт на митап в пятницу?",
    "TechHeads опять задержали начало",
]
keyword = "techheads"

def find_mentions(messages, keyword):
        
    return [message for message in messages if keyword.lower() in message.lower()]

found = find_mentions(messages, keyword)
print(found)
print(len(found))
print(find_mentions(messages, "AI"))