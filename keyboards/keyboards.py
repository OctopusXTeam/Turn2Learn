"""Модуль с клавиатурами для бота"""

from aiogram import types
from utils.constants import SUPPORTED_LANGUAGES
from locales.translations import TRANSLATIONS

def get_language_keyboard() -> types.InlineKeyboardMarkup:
    """Создает клавиатуру выбора языка"""
    keyboard = []
    row = []
    
    for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
        row.append(types.InlineKeyboardButton(
            text=lang_name,
            callback_data=f"lang_{lang_code}"
        ))
        
        if len(row) == 2:
            keyboard.append(row)
            row = []
            
    if row:  # Добавляем оставшиеся кнопки
        keyboard.append(row)
        
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_main_menu_keyboard(language: str) -> types.InlineKeyboardMarkup:
    """Создает клавиатуру главного меню"""
    keyboard = [
        [types.InlineKeyboardButton(
            text=TRANSLATIONS[language]['learn'],
            callback_data="learn"
        )],
        [types.InlineKeyboardButton(
            text=TRANSLATIONS[language]['my_cards'],
            callback_data="my_cards"
        )],
        [types.InlineKeyboardButton(
            text=TRANSLATIONS[language]['settings'],
            callback_data="settings"
        )],
        [types.InlineKeyboardButton(
            text=TRANSLATIONS[language]['language'],
            callback_data="change_language"
        )]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_settings_keyboard(language: str, front_languages: list, back_languages: list, show_learn_button: bool = False) -> types.InlineKeyboardMarkup:
    """Создает клавиатуру для настроек"""
    keyboard = []
    
    # Словарь с флагами для языков
    flags = {'ru': '🇷🇺', 'en': '🇬🇧', 'es': '🇪🇸', 'ro': '🇷🇴'}
    
    # Добавляем кнопки выбора языков
    for lang in ['ru', 'en', 'es', 'ro']:
        front_status = '✅' if lang in front_languages else '✖️'
        back_status = '✅' if lang in back_languages else '✖️'
        
        keyboard.append([
            types.InlineKeyboardButton(
                text=f"{front_status} {flags[lang]}",
                callback_data=f"front_{lang}"
            ),
            types.InlineKeyboardButton(
                text=f"{back_status} {flags[lang]}",
                callback_data=f"back_{lang}"
            )
        ])
    
    # Добавляем кнопки навигации
    keyboard.append([
        types.InlineKeyboardButton(
            text=TRANSLATIONS[language]['back_to_menu'],
            callback_data="back_to_menu"
        )
    ])
    
    # Добавляем кнопку уведомлений
    keyboard.append([
        types.InlineKeyboardButton(
            text=TRANSLATIONS[language]['notifications'],
            callback_data="notifications"
        )
    ])
    
    # Добавляем кнопку "Учить" только если выбраны языки с обеих сторон
    if front_languages and back_languages:
        keyboard.append([
            types.InlineKeyboardButton(
                text=TRANSLATIONS[language]['learn'],
                callback_data="learn"
            )
        ])
    
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_cards_keyboard(language: str, cards: list, page: int = 1, cards_per_page: int = 10) -> tuple[types.InlineKeyboardMarkup, str]:
    """Создает клавиатуру для отображения карточек с пагинацией."""
    keyboard = []
    total_pages = (len(cards) + cards_per_page - 1) // cards_per_page if cards else 1
    
    # Формируем заголовок в одну строку
    if not cards:
        page_counter = TRANSLATIONS[language]['my_cards']
    else:
        page_counter = (
            f"{TRANSLATIONS[language]['my_cards']} | "
            f"{TRANSLATIONS[language]['total_cards'].format(len(cards))} | "
            f"{TRANSLATIONS[language]['page_counter'].format(page, total_pages)}"
        )
    
    if not cards:
        # Добавляем кнопку "Пусто" если нет карточек
        keyboard.append([types.InlineKeyboardButton(
            text=TRANSLATIONS[language]['empty_button'],
            callback_data="add_card"
        )])
    else:
        start_idx = (page - 1) * cards_per_page
        end_idx = min(start_idx + cards_per_page, len(cards))
        
        # Добавляем карточки текущей страницы
        for card in cards[start_idx:end_idx]:
            translations = []
            for lang_code, word in card['translations'].items():
                if lang_code == 'ru':
                    translations.append(f"🇷🇺 {word}")
                elif lang_code == 'en':
                    translations.append(f"🇬🇧 {word}")
                elif lang_code == 'es':
                    translations.append(f"🇪🇸 {word}")
                elif lang_code == 'ro':
                    translations.append(f"🇷🇴 {word}")
            keyboard.append([types.InlineKeyboardButton(
                text=' | '.join(translations),
                callback_data=f"card_{card['id']}"
            )])
    
    # Кнопки навигации
    nav_buttons = []
    
    # Кнопка "Назад"
    if page == 1:
        nav_buttons.append(types.InlineKeyboardButton(
            text="•••",
            callback_data="page_0"
        ))
    else:
        nav_buttons.append(types.InlineKeyboardButton(
            text=TRANSLATIONS[language]['prev_page'],
            callback_data=f"page_{page-1}"
        ))
    
    # Кнопка "Добавить"
    nav_buttons.append(types.InlineKeyboardButton(
        text=TRANSLATIONS[language]['add_button'],
        callback_data="add_card"
    ))
    
    # Кнопка "Вперед"
    if page >= total_pages:
        nav_buttons.append(types.InlineKeyboardButton(
            text="•••",
            callback_data=f"page_{total_pages+1}"
        ))
    else:
        nav_buttons.append(types.InlineKeyboardButton(
            text=TRANSLATIONS[language]['next_page'],
            callback_data=f"page_{page+1}"
        ))
    
    keyboard.append(nav_buttons)
    
    # Добавляем кнопку возврата в меню
    keyboard.append([types.InlineKeyboardButton(
        text=TRANSLATIONS[language]['back_to_menu'],
        callback_data="back_to_menu"
    )])
    
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard), page_counter

def get_card_view_keyboard(language: str, card_id: int) -> types.InlineKeyboardMarkup:
    """Создает клавиатуру для просмотра карточки."""
    keyboard = []
    
    # Кнопки редактирования для каждого языка
    edit_buttons = [
        [
            types.InlineKeyboardButton(
                text=f"🇷🇺 {TRANSLATIONS[language]['edit_button']}", 
                callback_data=f"edit_{card_id}_ru"
            ),
            types.InlineKeyboardButton(
                text=f"🇬🇧 {TRANSLATIONS[language]['edit_button']}", 
                callback_data=f"edit_{card_id}_en"
            )
        ],
        [
            types.InlineKeyboardButton(
                text=f"🇪🇸 {TRANSLATIONS[language]['edit_button']}", 
                callback_data=f"edit_{card_id}_es"
            ),
            types.InlineKeyboardButton(
                text=f"🇷🇴 {TRANSLATIONS[language]['edit_button']}", 
                callback_data=f"edit_{card_id}_ro"
            )
        ]
    ]
    keyboard.extend(edit_buttons)
    
    # Кнопки удаления и возврата
    control_buttons = [
        types.InlineKeyboardButton(
            text=TRANSLATIONS[language]['delete_button'],
            callback_data=f"delete_{card_id}"
        ),
        types.InlineKeyboardButton(
            text=TRANSLATIONS[language]['back_button'],
            callback_data="back_to_cards"
        )
    ]
    keyboard.append(control_buttons)
    
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_add_card_keyboard(language: str, translations: dict = None) -> types.InlineKeyboardMarkup:
    """Создает клавиатуру для добавления новой карточки."""
    if translations is None:
        translations = {}
    
    keyboard = []
    
    # Кнопки добавления переводов
    keyboard.extend([
        [
            types.InlineKeyboardButton(
                text=f"🇷🇺 {TRANSLATIONS[language]['add_button']}", 
                callback_data="add_translation_ru"
            ),
            types.InlineKeyboardButton(
                text=f"🇬🇧 {TRANSLATIONS[language]['add_button']}", 
                callback_data="add_translation_en"
            )
        ],
        [
            types.InlineKeyboardButton(
                text=f"🇪🇸 {TRANSLATIONS[language]['add_button']}", 
                callback_data="add_translation_es"
            ),
            types.InlineKeyboardButton(
                text=f"🇷🇴 {TRANSLATIONS[language]['add_button']}", 
                callback_data="add_translation_ro"
            )
        ]
    ])
    
    # Кнопки GPT, сохранения и возврата
    control_buttons = [
        [types.InlineKeyboardButton(
            text="GPT",
            callback_data="add_translation_gpt"
        )],
        [
            types.InlineKeyboardButton(
                text=TRANSLATIONS[language]['save_button'],
                callback_data="save_card"
            ),
            types.InlineKeyboardButton(
                text=TRANSLATIONS[language]['back_button'],
                callback_data="back_to_cards"
            )
        ]
    ]
    keyboard.extend(control_buttons)
    
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard) 