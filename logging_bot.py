from datetime import datetime


def log_to_file(text):
    with open('bot_log.txt', 'a',encoding='UTF-8') as f:
        f.write(f"{datetime.now()} - {text}\n")


def try_ex_deco(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_to_file(f"ОШИБКА в {func.__name__}: {str(e)}")
            return None 
    return wrapper