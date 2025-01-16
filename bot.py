"""Основной файл бота"""

import os
import json
import time
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, StateFilter
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.keyboards import get_language_keyboard, get_main_menu_keyboard, get_settings_keyboard, get_cards_keyboard, get_card_view_keyboard, get_add_card_keyboard
from utils.data_manager import load_user_data, save_user_data, create_user, calculate_priority, select_next_card
from locales.translations import TRANSLATIONS, GPT_PROMPTS

def format_stats_message(stats, is_correct):
    """Форматирует сообщение со статистикой для показа пользователю"""
    total = stats['total_attempts']
    correct_percent = (stats['correct_answers'] / total * 100) if total > 0 else 0
    
    # Формируем звезды
    stars_count = round(correct_percent / 20)
    stars = "⭐️" * stars_count + "□" * (5 - stars_count)
    
    # Формируем сообщение
    result = "✅ +1" if is_correct else "❌ -1"
    return f"{result} | {stars} ({correct_percent:.0f}%) | {stats['correct_streak']}/15"

def create_statistics():
    """Создает начальную структуру статистики для карточки"""
    return {
        'total_attempts': 0,
        'correct_answers': 0,
        'wrong_answers': 0,
        'last_shown': None,
        'last_result': None,
        'correct_streak': 0,
        'wrong_streak': 0
    }

class CardStates(StatesGroup):
    waiting_for_translation = State()
    adding_card = State()
    adding_translation = State()
    waiting_for_gpt = State()
    learning = State()  # Новое состояние для режима обучения

# Загружаем токен из .env
load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

# Загружаем данные пользователей
user_data = load_user_data()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start - всегда показывает меню выбора языка"""
    # Отправляем новое сообщение с меню выбора языка
    await message.answer(
        TRANSLATIONS['ru']['welcome'],
        reply_markup=get_language_keyboard()
    )

@dp.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    """Обработчик возврата в главное меню"""
    user_id = str(callback.from_user.id)
    language = user_data[user_id]['interface_lang']
    
    # Возвращаемся в главное меню без проверки языков
    await callback.message.edit_text(
        TRANSLATIONS[language]['main_menu'],
        reply_markup=get_main_menu_keyboard(language)
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "change_language")
async def change_language(callback: types.CallbackQuery):
    """Обработчик кнопки смены языка"""
    user_id = str(callback.from_user.id)
    fresh_user_data = load_user_data()  # Загружаем свежие данные
    if user_id not in fresh_user_data:
        return
    
    # Обновляем глобальные данные
    global user_data
    user_data = fresh_user_data
    
    await callback.message.edit_text(
        TRANSLATIONS['ru']['welcome'],
        reply_markup=get_language_keyboard()
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "settings")
async def show_settings(callback: types.CallbackQuery):
    """Показывает меню настроек"""
    user_id = str(callback.from_user.id)
    fresh_user_data = load_user_data()  # Загружаем свежие данные
    if user_id not in fresh_user_data:
        return
    
    # Обновляем глобальные данные
    global user_data
    user_data = fresh_user_data
    
    language = user_data[user_id]['interface_lang']
    settings = user_data[user_id].get('settings', {})
    
    # Инициализируем списки языков, если их нет
    if 'front_languages' not in settings:
        settings['front_languages'] = []
    if 'back_languages' not in settings:
        settings['back_languages'] = []
    
    user_data[user_id]['settings'] = settings
    save_user_data(user_data)
    
    await callback.message.edit_text(
        TRANSLATIONS[language]['settings_menu'],
        reply_markup=get_settings_keyboard(
            language,
            settings['front_languages'],
            settings['back_languages']
        )
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith('lang_'))
async def language_choice(callback: types.CallbackQuery):
    user_id = str(callback.from_user.id)
    language = callback.data[5:]  # Получаем код языка (ru, en, es, ro)
    
    # Создаем или обновляем данные пользователя
    if user_id not in user_data:
        user_data[user_id] = create_user(user_id, language)
    else:
        user_data[user_id]['interface_lang'] = language
        # Проверяем наличие новых полей в настройках
        if 'settings' not in user_data[user_id]:
            user_data[user_id]['settings'] = {
                'daily_cards_limit': 20,
                'notification_enabled': True,
                'front_languages': [],
                'back_languages': []
            }
        elif 'front_languages' not in user_data[user_id]['settings']:
            user_data[user_id]['settings'].update({
                'front_languages': [],
                'back_languages': []
            })
    
    # Сохраняем данные
    save_user_data(user_data)
    
    # Редактируем текущее сообщение, заменяя его на главное меню
    await callback.message.edit_text(
        TRANSLATIONS[language]['main_menu'],
        reply_markup=get_main_menu_keyboard(language)
    )
    
    # Отвечаем на callback
    await callback.answer(TRANSLATIONS[language].get('language_selected', 'Язык выбран!'))

@dp.callback_query(lambda c: len(c.data.split('_')) == 2 and c.data.split('_')[0] in ['front', 'back'])
async def process_language_selection(callback: types.CallbackQuery):
    """Обработчик выбора языков для карточек"""
    user_id = str(callback.from_user.id)
    language = user_data[user_id]['interface_lang']
    settings = user_data[user_id]['settings']
    
    # Определяем, для какой стороны выбран язык
    side, lang_code = callback.data.split('_')
    target_list = f"{side}_languages"
    other_list = 'back_languages' if side == 'front' else 'front_languages'
    
    # Добавляем или удаляем язык из списка
    if lang_code in settings[target_list]:
        settings[target_list].remove(lang_code)
    else:
        # Если язык уже выбран в другом списке, удаляем его оттуда
        if lang_code in settings[other_list]:
            settings[other_list].remove(lang_code)
        settings[target_list].append(lang_code)
    
    save_user_data(user_data)
    
    # Обновляем клавиатуру
    await callback.message.edit_reply_markup(
        reply_markup=get_settings_keyboard(
            language,
            settings['front_languages'],
            settings['back_languages']
        )
    )
    await callback.answer()

# Обработчик остальных кнопок (заглушка)
@dp.callback_query(lambda c: c.data == "notifications")
async def process_callback(callback: types.CallbackQuery):
    """Временный обработчик для кнопки уведомлений"""
    user_id = str(callback.from_user.id)
    language = user_data[user_id]['interface_lang']
    
    # Пока просто показываем уведомление
    await callback.answer(f"🚧 {TRANSLATIONS[language]['notifications_in_progress']}")

@dp.callback_query(lambda c: c.data == "my_cards")
async def process_my_cards_button(callback: types.CallbackQuery):
    user_id = str(callback.from_user.id)
    fresh_user_data = load_user_data()  # Загружаем свежие данные
    if user_id not in fresh_user_data:
        return
    
    # Обновляем глобальные данные
    global user_data
    user_data = fresh_user_data
    
    language = user_data[user_id]['interface_lang']
    cards = user_data[user_id]['cards']
    
    keyboard, header = get_cards_keyboard(language, cards)
    await callback.message.edit_text(
        text=header,
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data.startswith('page_'))
async def change_cards_page(callback: types.CallbackQuery):
    user_id = str(callback.from_user.id)
    user_data = load_user_data()
    
    if user_id not in user_data:
        return
        
    language = user_data[user_id]['interface_lang']
    cards = user_data[user_id]['cards']
    page = int(callback.data.split('_')[1])
    total_pages = (len(cards) + 9) // 10  # 10 карточек на странице
    
    # Если всего одна страница
    if total_pages == 1:
        if page == 0:
            await callback.answer(TRANSLATIONS[language]['first_page'])
        else:
            await callback.answer(TRANSLATIONS[language]['last_page'])
        return
    
    # Если несколько страниц
    if page == 0:
        await callback.answer(TRANSLATIONS[language]['first_page'])
        return
    elif page > total_pages:
        await callback.answer(TRANSLATIONS[language]['last_page'])
        return
    
    # Переключаем на запрошенную страницу
    keyboard, header = get_cards_keyboard(language, cards, page)
    await callback.message.edit_text(
        text=header,
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "add_card")
async def add_card(callback: types.CallbackQuery, state: FSMContext):
    """Начинает процесс добавления новой карточки"""
    user_id = str(callback.from_user.id)
    fresh_user_data = load_user_data()  # Загружаем свежие данные
    if user_id not in fresh_user_data:
        return
    
    # Обновляем глобальные данные
    global user_data
    user_data = fresh_user_data
    
    language = user_data[user_id]['interface_lang']
    
    # Инициализируем пустой словарь для переводов
    await state.set_state(CardStates.adding_card)
    await state.update_data(translations={})
    
    # Формируем текст с текущими переводами
    text = f"{TRANSLATIONS[language]['add_new_card']}\n\n"
    text += "🇷🇺 -\n"
    text += "🇬🇧 -\n"
    text += "🇪🇸 -\n"
    text += "🇷🇴 -"
    
    # Показываем интерфейс добавления карточки
    await callback.message.edit_text(
        text=text,
        reply_markup=get_add_card_keyboard(language)
    )

@dp.callback_query(lambda c: c.data.startswith('add_translation_'), CardStates.adding_card)
async def start_translation_input(callback: types.CallbackQuery, state: FSMContext):
    """Начинает процесс ввода перевода для выбранного языка"""
    user_id = str(callback.from_user.id)
    language = user_data[user_id]['interface_lang']
    target_lang = callback.data.split('_')[2]
    
    # Если это GPT, показываем промт
    if target_lang == 'gpt':
        await show_gpt_prompt(callback, state)
        return
    
    # Сохраняем целевой язык и переходим к вводу перевода
    await state.update_data(current_lang=target_lang)
    await state.set_state(CardStates.adding_translation)
    
    # Показываем запрос на ввод перевода с кнопкой "Назад"
    lang_emoji = {'ru': '🇷🇺', 'en': '🇬🇧', 'es': '🇪🇸', 'ro': '🇷🇴'}[target_lang]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(
            text=TRANSLATIONS[language]['back_button'],
            callback_data="back_to_add_card"
        )
    ]])
    await callback.message.edit_text(
        text=TRANSLATIONS[language]['enter_translation'].format(lang_emoji),
        reply_markup=keyboard
    )

@dp.message(CardStates.adding_translation)
async def process_translation_input(message: types.Message, state: FSMContext):
    """Обрабатывает ввод перевода"""
    user_id = str(message.from_user.id)
    language = user_data[user_id]['interface_lang']
    
    # Получаем текущие данные
    data = await state.get_data()
    translations = data.get('translations', {})
    current_lang = data.get('current_lang')
    
    # Добавляем новый перевод
    new_translation = message.text.strip()
    translations[current_lang] = new_translation
    await state.update_data(translations=translations)
    await state.set_state(CardStates.adding_card)
    
    # Формируем текст с текущими переводами и проверяем на дубликаты
    text = f"{TRANSLATIONS[language]['add_new_card']}\n\n"
    for lang in ['ru', 'en', 'es', 'ro']:
        flag = {'ru': '🇷🇺', 'en': '🇬🇧', 'es': '🇪🇸', 'ro': '🇷🇴'}[lang]
        translation = translations.get(lang, '-')
        
        # Если есть перевод, проверяем на дубликаты
        if translation != '-':
            has_duplicate = False
            for card in user_data[user_id]['cards']:
                if card['translations'].get(lang, '').lower() == translation.lower():
                    has_duplicate = True
                    break
            
            if has_duplicate:
                text += f"{flag} {translation} - ⚠️ {TRANSLATIONS[language]['duplicate_translation']}\n"
            else:
                text += f"{flag} {translation}\n"
        else:
            text += f"{flag} -\n"
    
    text = text.rstrip()  # Убираем последний перенос строки
    
    # Показываем обновленный интерфейс добавления карточки
    await message.answer(
        text=text,
        reply_markup=get_add_card_keyboard(language, translations)
    )

@dp.callback_query(lambda c: c.data == "save_card", CardStates.adding_card)
async def save_new_card(callback: types.CallbackQuery, state: FSMContext):
    """Сохраняет новую карточку"""
    user_id = str(callback.from_user.id)
    fresh_user_data = load_user_data()  # Загружаем свежие данные
    if user_id not in fresh_user_data:
        return
    
    # Обновляем глобальные данные
    global user_data
    user_data = fresh_user_data
    
    language = user_data[user_id]['interface_lang']
    
    # Получаем переводы
    data = await state.get_data()
    translations = data.get('translations', {})
    
    # Проверяем количество переводов
    if len(translations) < 2:
        await callback.answer(TRANSLATIONS[language]['not_enough_translations'])
        return
    
    # Создаем новую карточку
    if 'cards' not in user_data[user_id]:
        user_data[user_id]['cards'] = []
    if 'last_card_id' not in user_data[user_id]:
        user_data[user_id]['last_card_id'] = 0
    
    new_card_id = user_data[user_id]['last_card_id'] + 1
    user_data[user_id]['cards'].append({
        'id': new_card_id,
        'translations': translations,
        'statistics': create_statistics()
    })
    user_data[user_id]['last_card_id'] = new_card_id
    
    # Сохраняем изменения
    save_user_data(user_data)
    
    # Очищаем состояние
    await state.clear()
    
    # Показываем уведомление и возвращаемся к списку карточек
    await callback.answer(TRANSLATIONS[language]['card_added'])
    await show_cards(callback.message, user_id, user_data)

@dp.callback_query(lambda c: c.data.startswith('card_'))
async def show_card(callback: types.CallbackQuery):
    """Показывает карточку для редактирования."""
    user_id = str(callback.from_user.id)
    card_id = int(callback.data.split('_')[1])
    
    user_data = load_user_data()
    if user_id not in user_data:
        return
    
    language = user_data[user_id]['interface_lang']
    
    # Находим карточку по ID
    card = next((card for card in user_data[user_id]['cards'] if card['id'] == card_id), None)
    if not card:
        return
    
    # Формируем текст с заголовком и переводами
    text = f"{TRANSLATIONS[language]['select_language_to_edit']}\n\n"
    text += '\n'.join([
        f"🇷🇺 {card['translations'].get('ru', '-')}",
        f"🇬🇧 {card['translations'].get('en', '-')}",
        f"🇪🇸 {card['translations'].get('es', '-')}",
        f"🇷🇴 {card['translations'].get('ro', '-')}"
    ])
    
    # Получаем клавиатуру для просмотра карточки
    keyboard = get_card_view_keyboard(language, card_id)
    
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data.startswith('edit_') and len(c.data.split('_')) == 3)
async def edit_card_translation(callback: types.CallbackQuery, state: FSMContext):
    """Запускает процесс редактирования перевода."""
    user_id = str(callback.from_user.id)
    _, card_id, lang = callback.data.split('_')
    card_id = int(card_id)
    
    user_data = load_user_data()
    if user_id not in user_data:
        return
    
    # Находим карточку
    card = next((card for card in user_data[user_id]['cards'] if card['id'] == card_id), None)
    if not card:
        return
        
    # Сохраняем данные для редактирования
    await state.update_data(card_id=card_id, edit_lang=lang)
    
    # Получаем текущий перевод
    current_translation = card['translations'].get(lang, '-')
    language = user_data[user_id]['interface_lang']
    
    # Создаем клавиатуру с кнопкой "Назад"
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(
            text=TRANSLATIONS[language]['back_button'],
            callback_data=f"back_to_card_{card_id}"
        )
    ]])
    
    # Запрашиваем новый перевод
    await callback.message.edit_text(
        text=f"{TRANSLATIONS[language]['current_translation']} {current_translation}\n" + 
             TRANSLATIONS[language]['edit_translation'].format(
                 {'ru': '🇷🇺', 'en': '🇬🇧', 'es': '🇪🇸', 'ro': '🇷🇴'}[lang]
             ),
        reply_markup=keyboard
    )
    
    # Устанавливаем состояние ожидания ввода
    await state.set_state('waiting_for_translation')

@dp.message(lambda message: True, StateFilter('waiting_for_translation'))
async def process_new_translation(message: types.Message, state: FSMContext):
    """Обрабатывает ввод нового перевода."""
    user_id = str(message.from_user.id)
    user_data = load_user_data()
    
    # Получаем сохраненные данные
    data = await state.get_data()
    card_id = data['card_id']
    edit_lang = data['edit_lang']
    
    # Находим и обновляем карточку
    card = next((card for card in user_data[user_id]['cards'] if card['id'] == card_id), None)
    if card:
        card['translations'][edit_lang] = message.text.strip()
        save_user_data(user_data)
    
    # Очищаем состояние
    await state.clear()
    
    # Показываем обновленную карточку
    translations_text = '\n'.join([
        f"🇷🇺 {card['translations'].get('ru', '-')}",
        f"🇬🇧 {card['translations'].get('en', '-')}",
        f"🇪🇸 {card['translations'].get('es', '-')}",
        f"🇷🇴 {card['translations'].get('ro', '-')}"
    ])
    
    keyboard = get_card_view_keyboard(user_data[user_id]['interface_lang'], card_id)
    
    await message.answer(
        text=translations_text,
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data.startswith('delete_') and len(c.data.split('_')) == 2)
async def confirm_delete_card(callback: types.CallbackQuery):
    """Запрашивает подтверждение удаления карточки."""
    user_id = str(callback.from_user.id)
    card_id = int(callback.data.split('_')[1])
    
    user_data = load_user_data()
    if user_id not in user_data:
        return
    
    # Находим карточку
    card = next((card for card in user_data[user_id]['cards'] if card['id'] == card_id), None)
    if not card:
        return
    
    # Формируем текст подтверждения
    text = TRANSLATIONS[user_data[user_id]['interface_lang']]['confirm_delete'] + '\n\n'
    text += '\n'.join([
        f"🇷🇺 {card['translations'].get('ru', '-')}",
        f"🇬🇧 {card['translations'].get('en', '-')}",
        f"🇪🇸 {card['translations'].get('es', '-')}",
        f"🇷🇴 {card['translations'].get('ro', '-')}"
    ])
    
    # Создаем клавиатуру для подтверждения
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(
            text=TRANSLATIONS[user_data[user_id]['interface_lang']]['yes_button'],
            callback_data=f"confirm_delete_{card_id}"
        ),
        types.InlineKeyboardButton(
            text=TRANSLATIONS[user_data[user_id]['interface_lang']]['no_button'],
            callback_data=f"card_{card_id}"
        )
    ]])
    
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data.startswith('confirm_delete_'))
async def delete_card(callback: types.CallbackQuery):
    """Удаляет карточку."""
    user_id = str(callback.from_user.id)
    card_id = int(callback.data.split('_')[2])
    
    user_data = load_user_data()
    if user_id not in user_data:
        return
    
    language = user_data[user_id]['interface_lang']
    
    # Удаляем карточку
    user_data[user_id]['cards'] = [
        card for card in user_data[user_id]['cards'] 
        if card['id'] != card_id
    ]
    
    # Если это была последняя карточка, сбрасываем last_card_id
    if not user_data[user_id]['cards']:
        user_data[user_id]['last_card_id'] = 0
        
    save_user_data(user_data)
    
    # Показываем уведомление об успешном удалении
    await callback.answer(TRANSLATIONS[language]['card_deleted'])
    
    try:
        # Показываем обновленный список карточек
        keyboard, header = get_cards_keyboard(language, user_data[user_id]['cards'])
        await callback.message.edit_text(
            text=header,
            reply_markup=keyboard
        )
    except Exception as e:
        # Если произошла ошибка при обновлении сообщения, отправляем новое
        keyboard, header = get_cards_keyboard(language, user_data[user_id]['cards'])
        await callback.message.answer(
            text=header,
            reply_markup=keyboard
        )

@dp.callback_query(lambda c: c.data == "back_to_cards")
async def back_to_cards_list(callback: types.CallbackQuery):
    """Возвращает к списку карточек."""
    user_id = str(callback.from_user.id)
    user_data = load_user_data()
    
    await show_cards(callback.message, user_id, user_data)

async def show_cards(message: types.Message, user_id: str, user_data: dict):
    """Показывает список карточек пользователя."""
    language = user_data[user_id]['interface_lang']
    cards = user_data[user_id]['cards']
    
    if not cards:
        await message.edit_text(
            text=TRANSLATIONS[language]['no_cards'],
            reply_markup=get_main_menu_keyboard(language)
        )
        return

    keyboard, header = get_cards_keyboard(language, cards)
    await message.edit_text(
        text=header,
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "back_to_add_card", CardStates.adding_translation)
async def back_to_add_card_from_translation(callback: types.CallbackQuery, state: FSMContext):
    """Возвращает к интерфейсу добавления карточки из режима ввода перевода"""
    user_id = str(callback.from_user.id)
    language = user_data[user_id]['interface_lang']
    
    # Получаем текущие переводы
    data = await state.get_data()
    translations = data.get('translations', {})
    
    # Возвращаемся к состоянию добавления карточки
    await state.set_state(CardStates.adding_card)
    
    # Формируем текст с текущими переводами
    text = f"{TRANSLATIONS[language]['add_new_card']}\n\n"
    for lang in ['ru', 'en', 'es', 'ro']:
        flag = {'ru': '🇷🇺', 'en': '🇬🇧', 'es': '🇪🇸', 'ro': '🇷🇴'}[lang]
        if lang in translations:
            text += f"{flag} {translations[lang]}\n"
        else:
            text += f"{flag} -\n"
    text = text.rstrip()
    
    # Показываем интерфейс добавления карточки
    await callback.message.edit_text(
        text=text,
        reply_markup=get_add_card_keyboard(language, translations)
    )

@dp.callback_query(lambda c: c.data.startswith('back_to_card_'), StateFilter('waiting_for_translation'))
async def back_to_card_from_edit(callback: types.CallbackQuery, state: FSMContext):
    """Возвращает к просмотру карточки из режима редактирования"""
    user_id = str(callback.from_user.id)
    card_id = int(callback.data.split('_')[3])
    language = user_data[user_id]['interface_lang']
    
    # Находим карточку
    card = next((card for card in user_data[user_id]['cards'] if card['id'] == card_id), None)
    if not card:
        return
    
    # Очищаем состояние
    await state.clear()
    
    # Формируем текст с переводами
    text = f"{TRANSLATIONS[language]['select_language_to_edit']}\n\n"
    text += '\n'.join([
        f"🇷🇺 {card['translations'].get('ru', '-')}",
        f"🇬🇧 {card['translations'].get('en', '-')}",
        f"🇪🇸 {card['translations'].get('es', '-')}",
        f"🇷🇴 {card['translations'].get('ro', '-')}"
    ])
    
    # Показываем карточку
    await callback.message.edit_text(
        text=text,
        reply_markup=get_card_view_keyboard(language, card_id)
    )

@dp.callback_query(lambda c: c.data == "add_translation_gpt")
async def show_gpt_prompt(callback: types.CallbackQuery, state: FSMContext):
    """Показывает промт для GPT"""
    user_id = str(callback.from_user.id)
    language = user_data[user_id]['interface_lang']
    
    # Получаем промт на выбранном языке
    prompt = GPT_PROMPTS[language]
    
    # Формируем сообщение с промтом
    text = (
        f"{TRANSLATIONS[language]['gpt_prompt_title']}\n\n"
        f"{TRANSLATIONS[language]['gpt_prompt_instruction']}\n\n"
        f"<pre>{prompt}</pre>\n\n"
        f"{TRANSLATIONS[language]['gpt_prompt_note']}\n\n"
        f"{TRANSLATIONS[language]['gpt_prompt_action']}"
    )
    
    # Создаем клавиатуру с кнопкой "Назад"
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(
            text=TRANSLATIONS[language]['back_button'],
            callback_data="back_to_add_card"
        )
    ]])
    
    # Отправляем сообщение с промтом
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    
    # Устанавливаем состояние ожидания ответа от GPT
    await state.set_state(CardStates.waiting_for_gpt)

@dp.message(CardStates.waiting_for_gpt)
async def process_gpt_response(message: types.Message, state: FSMContext):
    """Обрабатывает ответ от GPT"""
    user_id = str(message.from_user.id)
    language = user_data[user_id]['interface_lang']
    
    # Парсим ответ
    translations_list = []
    for line in message.text.strip().split('\n'):
        if not line.strip() or line.startswith('```'):
            continue
            
        # Парсим переводы из строки
        translations = {}
        parts = line.split('|')
        for part in parts:
            part = part.strip()
            if '🇷🇺' in part:
                translations['ru'] = part.split(':')[1].strip()
            elif '🇬🇧' in part:
                translations['en'] = part.split(':')[1].strip()
            elif '🇪🇸' in part:
                translations['es'] = part.split(':')[1].strip()
            elif '🇷🇴' in part:
                translations['ro'] = part.split(':')[1].strip()
        
        if translations:
            translations_list.append(translations)
    
    # Разделяем на новые и существующие карточки
    new_cards = []
    duplicate_cards = []
    
    for trans in translations_list:
        is_duplicate = False
        for card in user_data[user_id]['cards']:
            if all(trans.get(lang, '').lower() == card['translations'].get(lang, '').lower() for lang in ['ru', 'en', 'es', 'ro']):
                duplicate_cards.append(trans)
                is_duplicate = True
                break
        if not is_duplicate:
            new_cards.append(trans)
    
    # Сохраняем в состояние только новые карточки
    await state.update_data(gpt_translations=new_cards)
    
    # Формируем текст предпросмотра
    text = f"{TRANSLATIONS[language]['gpt_cards_found'].format(len(new_cards))}\n\n"
    
    # Добавляем новые карточки
    for trans in new_cards:
        text += (
            f"🇷🇺 {trans.get('ru', '-')} | "
            f"🇬🇧 {trans.get('en', '-')} | "
            f"🇪🇸 {trans.get('es', '-')} | "
            f"🇷🇴 {trans.get('ro', '-')}\n"
        )
    
    # Если есть дубликаты, добавляем их отдельным списком
    if duplicate_cards:
        text += f"\n{TRANSLATIONS[language]['duplicate_cards_warning']}:\n\n"
        for trans in duplicate_cards:
            text += (
                f"🇷🇺 {trans.get('ru', '-')} | "
                f"🇬🇧 {trans.get('en', '-')} | "
                f"🇪🇸 {trans.get('es', '-')} | "
                f"🇷🇴 {trans.get('ro', '-')}\n"
            )
    
    # Создаем клавиатуру с кнопками "Сохранить" и "Назад"
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(
            text=TRANSLATIONS[language]['save_button'],
            callback_data="save_gpt_cards"
        ),
        types.InlineKeyboardButton(
            text=TRANSLATIONS[language]['back_button'],
            callback_data="back_to_add_card"
        )
    ]])
    
    await message.answer(
        text=text,
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "save_gpt_cards")
async def save_gpt_cards(callback: types.CallbackQuery, state: FSMContext):
    """Сохраняет карточки, сгенерированные через GPT"""
    user_id = str(callback.from_user.id)
    language = user_data[user_id]['interface_lang']
    
    # Получаем переводы из состояния
    data = await state.get_data()
    translations_list = data.get('gpt_translations', [])
    
    # Добавляем карточки
    if 'cards' not in user_data[user_id]:
        user_data[user_id]['cards'] = []
    if 'last_card_id' not in user_data[user_id]:
        user_data[user_id]['last_card_id'] = 0
    
    for translations in translations_list:
        new_card_id = user_data[user_id]['last_card_id'] + 1
        user_data[user_id]['cards'].append({
            'id': new_card_id,
            'translations': translations,
            'statistics': create_statistics()
        })
        user_data[user_id]['last_card_id'] = new_card_id
    
    # Сохраняем изменения
    save_user_data(user_data)
    
    # Очищаем состояние
    await state.clear()
    
    # Показываем уведомление и возвращаемся к списку карточек
    await callback.answer(TRANSLATIONS[language]['card_added'])
    await show_cards(callback.message, user_id, user_data)

@dp.callback_query(lambda c: c.data == "back_to_add_card", CardStates.waiting_for_gpt)
async def back_to_add_card_from_gpt(callback: types.CallbackQuery, state: FSMContext):
    """Возвращает к интерфейсу добавления карточки из режима GPT"""
    user_id = str(callback.from_user.id)
    language = user_data[user_id]['interface_lang']
    
    # Получаем текущие переводы
    data = await state.get_data()
    translations = data.get('translations', {})
    
    # Возвращаемся к состоянию добавления карточки
    await state.set_state(CardStates.adding_card)
    
    # Формируем текст с текущими переводами
    text = f"{TRANSLATIONS[language]['add_new_card']}\n\n"
    for lang in ['ru', 'en', 'es', 'ro']:
        flag = {'ru': '🇷🇺', 'en': '🇬🇧', 'es': '🇪🇸', 'ro': '🇷🇴'}[lang]
        if lang in translations:
            text += f"{flag} {translations[lang]}\n"
        else:
            text += f"{flag} -\n"
    text = text.rstrip()
    
    # Показываем интерфейс добавления карточки
    await callback.message.edit_text(
        text=text,
        reply_markup=get_add_card_keyboard(language, translations)
    )

@dp.callback_query(lambda c: c.data == "learn")
async def start_learning(callback: types.CallbackQuery, state: FSMContext):
    """Начинает процесс обучения"""
    user_id = str(callback.from_user.id)
    fresh_user_data = load_user_data()  # Загружаем свежие данные
    if user_id not in fresh_user_data:
        return
    
    # Обновляем глобальные данные
    global user_data
    user_data = fresh_user_data
    
    language = user_data[user_id]['interface_lang']
    settings = user_data[user_id].get('settings', {})
    
    # Проверяем настройки языков
    if not settings.get('front_languages') or not settings.get('back_languages'):
        await callback.message.edit_text(
            TRANSLATIONS[language]['settings_menu'],
            reply_markup=get_settings_keyboard(
                language,
                settings.get('front_languages', []),
                settings.get('back_languages', [])
            )
        )
        return
    
    # Проверяем наличие карточек с выбранными языками
    valid_cards = []
    for card in user_data[user_id].get('cards', []):
        # Проверяем, есть ли хотя бы один перевод для front и back языков
        has_front = any(card['translations'].get(lang) for lang in settings['front_languages'])
        has_back = any(card['translations'].get(lang) for lang in settings['back_languages'])
        if has_front and has_back:
            valid_cards.append(card)
    
    if not valid_cards:
        await callback.answer(TRANSLATIONS[language]['no_cards_for_selected_languages'], show_alert=True)
        return
    
    # Устанавливаем состояние обучения
    await state.set_state(CardStates.learning)
    
    # Показываем первую карточку
    await show_learning_card(callback.message, user_id, state)

async def show_learning_card(message: types.Message, user_id: str, state: FSMContext):
    """Показывает карточку для изучения"""
    language = user_data[user_id]['interface_lang']
    settings = user_data[user_id]['settings']
    flags = {'ru': '🇷🇺', 'en': '🇬🇧', 'es': '🇪🇸', 'ro': '🇷🇴'}
    
    # Получаем ID текущей карточки из состояния
    data = await state.get_data()
    current_card_id = data.get('current_card_id')
    
    # Выбираем следующую карточку с помощью нового алгоритма
    card = select_next_card(user_id, current_card_id, user_data)
    
    # Сохраняем ID текущей карточки в состоянии
    await state.update_data(current_card_id=card['id'])
    
    # Формируем текст сообщения
    text = f"{TRANSLATIONS[language]['how_to_translate']}\n\n"
    
    # Показываем слово на выбранных языках с передней стороны
    for front_lang in settings['front_languages']:
        if translation := card['translations'].get(front_lang):
            text += f"{flags[front_lang]} {translation}\n"
    
    text += f"\n{TRANSLATIONS[language]['translation']}:\n"
    
    # Показываем переводы на выбранных языках с обратной стороны
    for back_lang in settings['back_languages']:
        if translation := card['translations'].get(back_lang):
            text += f"{flags[back_lang]} ||{translation}||\n"
    
    # Создаем клавиатуру с переводами кнопок
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=TRANSLATIONS[language]['back_to_menu'], callback_data="back_to_menu")],
        [types.InlineKeyboardButton(text=TRANSLATIONS[language]['wrong'], callback_data="answer_wrong")],
        [types.InlineKeyboardButton(text=TRANSLATIONS[language]['correct'], callback_data="answer_correct")]
    ])
    
    try:
        # Сначала отправляем новое сообщение
        new_message = await message.answer(text, reply_markup=keyboard, parse_mode="MarkdownV2")
        try:
            # Затем пытаемся удалить старое
            await message.delete()
        except Exception:
            pass  # Игнорируем ошибки при удалении
        return new_message
    except Exception as e:
        # В случае ошибки просто отправляем новое сообщение
        return await message.answer(text, reply_markup=keyboard, parse_mode="MarkdownV2")

@dp.callback_query(lambda c: c.data == "back_to_menu", CardStates.learning)
async def back_to_menu_from_learning(callback: types.CallbackQuery, state: FSMContext):
    """Возвращает пользователя в главное меню из режима обучения"""
    user_id = str(callback.from_user.id)
    language = user_data[user_id]['interface_lang']
    
    # Очищаем состояние
    await state.clear()
    
    # Возвращаемся в главное меню
    await callback.message.edit_text(
        TRANSLATIONS[language]['main_menu'],
        reply_markup=get_main_menu_keyboard(language)
    )

@dp.callback_query(lambda c: c.data in ["answer_correct", "answer_wrong"], CardStates.learning)
async def process_answer(callback: types.CallbackQuery, state: FSMContext):
    """Обрабатывает ответ пользователя (верно/неверно)"""
    user_id = str(callback.from_user.id)
    is_correct = callback.data == "answer_correct"
    
    # Получаем ID текущей карточки из состояния
    data = await state.get_data()
    current_card_id = data.get('current_card_id')
    
    # Находим текущую карточку
    current_card = next(
        (card for card in user_data[user_id]['cards'] if card['id'] == current_card_id),
        None
    )
    
    if current_card:
        # Инициализируем статистику, если её нет
        if 'statistics' not in current_card:
            current_card['statistics'] = create_statistics()
        
        stats = current_card['statistics']
        
        # Обновляем статистику
        stats['total_attempts'] += 1
        if is_correct:
            stats['correct_answers'] += 1
            stats['correct_streak'] += 1
            stats['wrong_streak'] = 0
        else:
            stats['wrong_answers'] += 1
            stats['wrong_streak'] += 1
            stats['correct_streak'] = 0
        
        stats['last_shown'] = time.time()
        stats['last_result'] = is_correct
        
        # Сохраняем изменения
        save_user_data(user_data)
        
        # Показываем всплывающее сообщение со статистикой
        stats_message = format_stats_message(stats, is_correct)
        await callback.answer(stats_message, show_alert=False)
    
    # Показываем следующую карточку
    await show_learning_card(callback.message, user_id, state)

async def main():
    """Запуск бота"""
    print("Bot started!")  # Добавляем сообщение о запуске
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Error: {e}")  # Добавляем вывод ошибок

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped!")
    except Exception as e:
        print(f"Fatal error: {e}") 