from datetime import datetime
import functools

from controller import get_current_time


def log_to_file(text):
    with open('bot_log.txt', 'a',encoding='UTF-8') as f:
        f.write(f"{get_current_time} - {text}\n")


def try_ex_deco(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            log_to_file(f"ОШИБКА в {func.__name__}: {str(e)}")
            return None
    return wrapper


def try_ex_deco_sync(func):
    """Декоратор для синхронных функций"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_to_file(f"ОШИБКА в {func.__name__}: {str(e)}")
            return None
    return wrapper