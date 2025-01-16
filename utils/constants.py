"""Файл с константами проекта"""

import os

# Пути к файлам
DATA_DIR = 'data'
USER_DATA_FILE = os.path.join(DATA_DIR, 'user_data.json')
DEFAULT_CARDS_FILE = os.path.join(DATA_DIR, 'default_cards.json')

# Настройки по умолчанию
DEFAULT_SETTINGS = {
    'daily_cards_limit': 20,
    'notification_enabled': True
}

# Поддерживаемые языки
SUPPORTED_LANGUAGES = {
    'ru': '🇷🇺 Русский',
    'en': '🇬🇧 English',
    'es': '🇪🇸 Español',
    'ro': '🇷🇴 Română'
} 