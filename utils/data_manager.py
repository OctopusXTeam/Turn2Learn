"""Модуль для работы с данными пользователей"""

import json
import os
from utils.constants import DATA_DIR, USER_DATA_FILE, DEFAULT_CARDS_FILE
import time
import random

def ensure_data_dir():
    """Создает директорию для данных и инициализирует файлы, если они не существуют"""
    # Создаем директорию, если её нет
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # Проверяем и инициализируем файл с данными пользователей
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=4)
    else:
        # Проверяем, не пустой ли файл
        if os.path.getsize(USER_DATA_FILE) == 0:
            with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)

def load_default_cards():
    """Загружает шаблонные карточки из файла"""
    if os.path.exists(DEFAULT_CARDS_FILE):
        with open(DEFAULT_CARDS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('cards', [])
    return []

def load_user_data():
    """Загружает данные пользователей из файла"""
    ensure_data_dir()
    with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_user_data(data):
    """Сохраняет данные пользователей в файл"""
    ensure_data_dir()
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def create_user(user_id: str, language: str) -> dict:
    """Создает структуру данных для нового пользователя"""
    default_cards = load_default_cards()
    
    # Устанавливаем языки карточек в зависимости от выбранного языка интерфейса
    if language == 'ru':
        front_lang = ['en']  # Английский на лицевой
        back_lang = ['ru']   # Русский на обратной
    elif language == 'en':
        front_lang = ['es']  # Испанский на лицевой
        back_lang = ['en']   # Английский на обратной
    elif language == 'es':
        front_lang = ['en']  # Английский на лицевой
        back_lang = ['es']   # Испанский на обратной
    elif language == 'ro':
        front_lang = ['en']  # Английский на лицевой
        back_lang = ['ro']   # Румынский на обратной
    
    return {
        'interface_lang': language,
        'settings': {
            'front_languages': front_lang,
            'back_languages': back_lang
        },
        'cards': default_cards,
        'last_card_id': len(default_cards)
    } 

def calculate_priority(card, last_card_id=None):
    """Вычисляет приоритет карточки для показа"""
    priority = 0
    current_time = time.time()
    
    # Если это та же карточка, что была показана последней - исключаем её
    if last_card_id and card['id'] == last_card_id:
        return -1
    
    # Базовый приоритет на основе времени (0-30 баллов)
    hours_since_last = (current_time - (card['statistics']['last_shown'] or 0)) / 3600
    if card['statistics']['last_shown'] is None:  # Новая карточка
        priority += 30
    elif hours_since_last > 12:    # Давно не показывали
        priority += 20
    elif hours_since_last > 1:     # Показывали недавно
        priority += 10
    
    # Фактор ошибок (0-30 баллов)
    total = card['statistics']['total_attempts']
    if total > 0:
        error_rate = card['statistics']['wrong_answers'] / total
        if error_rate > 0.5:          # Больше 50% ошибок
            priority += 30
        elif error_rate > 0.3:        # Больше 30% ошибок
            priority += 20
        elif error_rate > 0.1:        # Больше 10% ошибок
            priority += 10
    
    # Фактор стрика ошибок (0-15 баллов)
    if card['statistics']['wrong_streak'] >= 2:
        priority += 15
    elif card['statistics']['wrong_streak'] == 1:
        priority += 7
    
    # Случайный фактор (0-35 баллов)
    priority += random.randint(0, 35)
    
    return priority 

def select_next_card(user_id, current_card_id=None, user_data=None):
    """Выбирает следующую карточку для показа"""
    if not user_data:
        user_data = load_user_data()
        
    cards = user_data[user_id]['cards']
    
    # Если карточек нет, возвращаем None
    if not cards:
        return None
        
    # Если карточка всего одна, возвращаем её
    if len(cards) == 1:
        return cards[0]
    
    # Вычисляем приоритеты для всех карточек
    cards_with_priority = [
        (card, calculate_priority(card, current_card_id))
        for card in cards
    ]
    
    # Сортируем по приоритету (исключая карточки с приоритетом -1)
    valid_cards = [(c, p) for c, p in cards_with_priority if p >= 0]
    
    # Если все карточки имеют приоритет -1, сбрасываем исключение последней карточки
    if not valid_cards:
        valid_cards = [(c, calculate_priority(c)) for c in cards]
    
    # Сортируем по приоритету
    valid_cards.sort(key=lambda x: x[1], reverse=True)
    
    # Возвращаем карточку с наивысшим приоритетом
    return valid_cards[0][0] 