"""Модуль с переводами для бота"""

TRANSLATIONS = {
    'ru': {
        'welcome': "🇷🇺 Выберите язык интерфейса бота\n"
                  "🇬🇧 Choose bot interface language\n"
                  "🇪🇸 Seleccione el idioma de la interfaz del bot\n"
                  "🇷🇴 Selectați limba interfeței botului",
        'main_menu': '🌟 Главное меню\n\n'
                    '📚 Учить — начать обучение\n'
                    '🎴 Мои карточки — создавайте и редактируйте карточки\n'
                    '⚙️ Настройки — настройте режим обучения\n'
                    '🌍 Язык — измените язык интерфейса бота',
        'learn': '📚 Учить',
        'my_cards': '🎴 Мои карточки',
        'settings': '⚙️ Настройки',
        'language': '🌍 Язык',
        'language_selected': '✅ Язык успешно изменён!',
        'notifications': '🔔 Уведомления',
        'back_to_menu': '◀️ Вернуться в меню',
        'settings_menu': '⚙️ Настройки\n\n'
                        'Выберите языки для изучения:\n'
                        'Левый столбец - языки для передней стороны карточек\n'
                        'Правый столбец - языки для обратной стороны\n\n'
                        '✅ - язык выбран\n'
                        '✖️ - язык не выбран',
        'select_languages_warning': 'Пожалуйста, выберите хотя бы один язык для каждой стороны карточек.',
        'learn_in_progress': 'Обучение (в разработке)',
        'notifications_in_progress': 'Уведомления (в разработке)',
        'add_card': '➕ Добавить карточку',
        'delete_card': '🗑️ Удалить',
        'no_cards': 'У вас пока нет карточек.\nНажмите ➕ чтобы добавить первую карточку!',
        'card_added': 'Карточка добавлена!',
        'card_deleted': '🗑️Карточка удалена!',
        'page_counter': 'Страница {} из {}',
        'next_page': 'Вперед ▶️',
        'prev_page': '◀️ Назад',
        'add_button': '➕ Добавить',
        'first_page': '⚠️ Это первая страница',
        'last_page': '⚠️ Это последняя страница',
        'edit_translation': 'Введите новый перевод для {}',
        'confirm_delete': '⚠️ Вы уверены, что хотите удалить карточку?',
        'edit_button': 'Редактировать',
        'delete_button': '🗑️ Удалить',
        'back_button': '◀️ Назад',
        'yes_button': '✅ Да',
        'no_button': '❌ Нет',
        'view_card': 'Карточка {}',
        'select_language_to_edit': 'На каком языке хотите отредактировать слово?',
        'save_button': '💾 Сохранить',
        'add_new_card': 'Добавьте новую карточку',
        'enter_translation': 'Введите перевод на {}',
        'not_enough_translations': '⚠️ Добавьте хотя бы два перевода',
        'current_translation': 'Текущий перевод:',
        'gpt_prompt_title': 'Для добавления карточек с помощью GPT',
        'gpt_prompt_instruction': 'Отправь в Chat GPT этот промт:',
        'gpt_prompt_note': '⚠️ ВАЖНО! Ты можешь изменить кол-во слов и категорию',
        'gpt_prompt_action': 'Просто отправь мне то что тебе ответит GPT',
        'gpt_cards_found': 'Найдено {} новых карточек:',
        'duplicate_cards_warning': 'Эти карточки уже были, они не будут добавлены повторно',
        'duplicate_translation': 'Такой перевод уже существует',
        'how_to_translate': 'Как переводится это слово?',
        'translation': 'Перевод',
        'no_cards': '⚠️ У вас пока нет карточек для изучения',
        'select_languages_warning': '⚠️ Пожалуйста, выберите языки для изучения в настройках',
        'wrong': '❌ Неверно',
        'correct': '✅ Верно',
        'empty_button': 'Пусто',
        'no_cards_for_selected_languages': '⚠️ Нет карточек с выбранными языками.\n\n Добавьте карточки или измените настройки',
        'total_cards': 'Всего {} карточек'
    },
    'en': {
        'welcome': "🇷🇺 Выберите язык интерфейса бота\n"
                  "🇬🇧 Choose bot interface language\n"
                  "🇪🇸 Seleccione el idioma de la interfaz del bot\n"
                  "🇷🇴 Selectați limba interfeței botului",
        'main_menu': '🌟 Main Menu\n\n'
                    '📚 Learn — start learning\n'
                    '🎴 My Cards — create and edit your word collections\n'
                    '⚙️ Settings — configure learning mode\n'
                    '🌍 Language — change bot interface language',
        'learn': '📚 Learn',
        'my_cards': '🎴 My Cards',
        'settings': '⚙️ Settings',
        'language': '🌍 Language',
        'language_selected': '✅ Language changed successfully!',
        'notifications': '🔔 Notifications',
        'back_to_menu': '◀️ Back to Menu',
        'settings_menu': '⚙️ Settings\n\n'
                        'Select languages for learning:\n'
                        'Left column - languages for card front\n'
                        'Right column - languages for card back\n\n'
                        '✅ - language selected\n'
                        '✖️ - language not selected',
        'select_languages_warning': 'Please select at least one language for each side of the cards.',
        'learn_in_progress': 'Learn (in development)',
        'notifications_in_progress': 'Notifications (in development)',
        'add_card': '➕ Add card',
        'delete_card': '🗑️ Delete',
        'no_cards': 'You don\'t have any cards yet.\nPress ➕ to add your first card!',
        'card_added': 'Card added!',
        'card_deleted': '🗑️Card deleted!',
        'page_counter': 'Page {} of {}',
        'next_page': 'Next ▶️',
        'prev_page': '◀️ Back',
        'add_button': '➕ Add',
        'first_page': '⚠️ This is the first page',
        'last_page': '⚠️ This is the last page',
        'edit_translation': 'Enter new translation for {}',
        'confirm_delete': '⚠️ Are you sure you want to delete this card?',
        'edit_button': 'Edit',
        'delete_button': '🗑️ Delete',
        'back_button': '◀️ Back',
        'yes_button': '✅ Yes',
        'no_button': '❌ No',
        'view_card': 'Card {}',
        'select_language_to_edit': 'In which language would you like to edit the word?',
        'save_button': '💾 Save',
        'add_new_card': 'Add new card',
        'enter_translation': 'Enter translation in {}',
        'not_enough_translations': '⚠️ Add at least two translations',
        'current_translation': 'Current translation:',
        'gpt_prompt_title': 'To add cards using GPT',
        'gpt_prompt_instruction': 'Send this prompt to Chat GPT:',
        'gpt_prompt_note': '⚠️ IMPORTANT! You can change the number of words and category',
        'gpt_prompt_action': 'Just send me what GPT replies to you',
        'gpt_cards_found': 'Found {} new cards:',
        'duplicate_cards_warning': 'These cards already exist, they will not be added again',
        'duplicate_translation': 'This translation already exists',
        'how_to_translate': 'How do you translate this word?',
        'translation': 'Translation',
        'no_cards': '⚠️ You don\'t have any cards to learn yet',
        'select_languages_warning': '⚠️ Please select languages for learning in settings',
        'wrong': '❌ Wrong',
        'correct': '✅ Correct',
        'empty_button': 'Empty',
        'no_cards_for_selected_languages': '⚠️ No cards with selected languages.\nAdd cards or change language settings',
        'total_cards': 'Total {} cards'
    },
    'es': {
        'welcome': "🇷🇺 Выберите язык интерфейса бота\n"
                  "🇬🇧 Choose bot interface language\n"
                  "🇪🇸 Seleccione el idioma de la interfaz del bot\n"
                  "🇷🇴 Selectați limba interfeței botului",
        'main_menu': '🌟 Menú Principal\n\n'
                    '📚 Aprender — comenzar a aprender\n'
                    '🎴 Mis Tarjetas — crea y edita tus colecciones de palabras\n'
                    '⚙️ Ajustes — configura el modo de aprendizaje\n'
                    '🌍 Idioma — cambia el idioma de la interfaz del bot',
        'learn': '📚 Aprender',
        'my_cards': '🎴 Mis Tarjetas',
        'settings': '⚙️ Ajustes',
        'language': '🌍 Idioma',
        'language_selected': '✅ ¡Idioma cambiado con éxito!',
        'notifications': '🔔 Notificaciones',
        'back_to_menu': '◀️ Volver al Menú',
        'settings_menu': '⚙️ Ajustes\n\n'
                        'Selecciona idiomas para aprender:\n'
                        'Columna izquierda - idiomas para el frente de la tarjeta\n'
                        'Columna derecha - idiomas para el reverso de la tarjeta\n\n'
                        '✅ - idioma seleccionado\n'
                        '✖️ - idioma no seleccionado',
        'select_languages_warning': 'Por favor, selecciona al menos un idioma para cada lado de las tarjetas.',
        'learn_in_progress': 'Aprender (en desarrollo)',
        'notifications_in_progress': 'Notificaciones (en desarrollo)',
        'add_card': '➕ Añadir tarjeta',
        'delete_card': '🗑️ Eliminar',
        'no_cards': '¡Aún no tienes tarjetas.\nPresiona ➕ para añadir tu primera tarjeta!',
        'card_added': '¡Tarjeta añadida!',
        'card_deleted': '¡🗑️Tarjeta eliminada!',
        'page_counter': 'Página {} de {}',
        'next_page': 'Siguiente ▶️',
        'prev_page': '◀️ Atrás',
        'add_button': '➕ Añadir',
        'first_page': '⚠️ Esta es la primera página',
        'last_page': '⚠️ Esta es la última página',
        'edit_translation': 'Ingrese nueva traducción para {}',
        'confirm_delete': '⚠️ ¿Está seguro de que desea eliminar esta tarjeta?',
        'edit_button': 'Editar',
        'delete_button': '🗑️ Eliminar',
        'back_button': '◀️ Volver',
        'yes_button': '✅ Sí',
        'no_button': '❌ No',
        'view_card': 'Tarjeta {}',
        'select_language_to_edit': '¿En qué idioma desea editar la palabra?',
        'save_button': '💾 Guardar',
        'add_new_card': 'Añadir nueva tarjeta',
        'enter_translation': 'Ingrese la traducción en {}',
        'not_enough_translations': '⚠️ Agregue al menos dos traducciones',
        'current_translation': 'Traducción actual:',
        'gpt_prompt_title': 'Para añadir tarjetas usando GPT',
        'gpt_prompt_instruction': 'Envía este prompt a Chat GPT:',
        'gpt_prompt_note': '⚠️ ¡IMPORTANTE! Puedes cambiar el número de palabras y la categoría',
        'gpt_prompt_action': 'Solo envíame lo que GPT te responda',
        'gpt_cards_found': 'Se encontraron {} tarjetas nuevas:',
        'duplicate_cards_warning': 'Estas tarjetas ya existen, no se agregarán nuevamente',
        'duplicate_translation': 'Esta traducción ya existe',
        'how_to_translate': '¿Cómo se traduce esta palabra?',
        'translation': 'Traducción',
        'no_cards': '⚠️ Aún no tienes tarjetas para aprender',
        'select_languages_warning': '⚠️ Por favor, selecciona los idiomas para aprender en la configuración',
        'wrong': '❌ Incorrecto',
        'correct': '✅ Correcto',
        'empty_button': 'Vacío',
        'no_cards_for_selected_languages': '⚠️ No hay tarjetas con los idiomas seleccionados.\nAgrega tarjetas o cambia la configuración de idiomas',
        'total_cards': 'Total {} tarjetas'
    },
    'ro': {
        'welcome': "🇷🇺 Выберите язык интерфейса бота\n"
                  "🇬🇧 Choose bot interface language\n"
                  "🇪🇸 Seleccione el idioma de la interfaz del bot\n"
                  "🇷🇴 Selectați limba interfeței botului",
        'main_menu': '🌟 Meniu Principal\n\n'
                    '📚 Învață — începe să înveți\n'
                    '🎴 Cardurile Mele — creează și editează colecțiile tale de cuvinte\n'
                    '⚙️ Setări — configurează modul de învățare\n'
                    '🌍 Limbă — schimbă limba interfeței botului',
        'learn': '📚 Învață',
        'my_cards': '🎴 Cardurile Mele',
        'settings': '⚙️ Setări',
        'language': '🌍 Limbă',
        'language_selected': '✅ Limba a fost schimbată cu succes!',
        'notifications': '🔔 Notificări',
        'back_to_menu': '◀️ Înapoi la Meniu',
        'settings_menu': '⚙️ Setări\n\n'
                        'Selectați limbile pentru învățare:\n'
                        'Coloana stângă - limbi pentru fața cardului\n'
                        'Coloana dreaptă - limbi pentru spatele cardului\n\n'
                        '✅ - limbă selectată\n'
                        '✖️ - limbă neselectată',
        'select_languages_warning': 'Vă rugăm să selectați cel puțin o limbă pentru fiecare parte a cardurilor.',
        'learn_in_progress': 'Învață (în dezvoltare)',
        'notifications_in_progress': 'Notificări (în dezvoltare)',
        'add_card': '➕ Adăugați card',
        'delete_card': '🗑️ Șterge',
        'no_cards': 'Nu aveți carduri încă.\nApăsați ➕ pentru a adăuga primul card!',
        'card_added': 'Card adăugat!',
        'card_deleted': '🗑️Card șters!',
        'page_counter': 'Pagina {} din {}',
        'next_page': 'Înainte ▶️',
        'prev_page': '◀️ Înapoi',
        'add_button': '➕ Adăugați',
        'first_page': '⚠️ Aceasta este prima pagină',
        'last_page': '⚠️ Aceasta este ultima pagină',
        'edit_translation': 'Introduceți noua traducere pentru {}',
        'confirm_delete': '⚠️ Sigur doriți să ștergeți acest card?',
        'edit_button': 'Editare',
        'delete_button': '🗑️ Șterge',
        'back_button': '◀️ Înapoi',
        'yes_button': '✅ Da',
        'no_button': '❌ Nu',
        'view_card': 'Card {}',
        'select_language_to_edit': 'În ce limbă doriți să editați cuvântul?',
        'save_button': '💾 Salvează',
        'add_new_card': 'Adăugați un card nou',
        'enter_translation': 'Introduceți traducerea în {}',
        'not_enough_translations': '⚠️ Adăugați cel puțin două traduceri',
        'current_translation': 'Traducerea curentă:',
        'gpt_prompt_title': 'Pentru a adăuga carduri folosind GPT',
        'gpt_prompt_instruction': 'Trimite acest prompt la Chat GPT:',
        'gpt_prompt_note': '⚠️ IMPORTANT! Poți schimba numărul de cuvinte și categoria',
        'gpt_prompt_action': 'Doar trimite-mi ce îți răspunde GPT',
        'gpt_cards_found': 'S-au găsit {} carduri noi:',
        'duplicate_cards_warning': 'Aceste carduri există deja, nu vor fi adăugate din nou',
        'duplicate_translation': 'Această traducere există deja',
        'how_to_translate': 'Cum se traduce acest cuvânt?',
        'translation': 'Traducere',
        'no_cards': '⚠️ Nu ai încă carduri pentru învățare',
        'select_languages_warning': '⚠️ Te rog selectează limbile pentru învățare în setări',
        'wrong': '❌ Greșit',
        'correct': '✅ Corect',
        'empty_button': 'Gol',
        'no_cards_for_selected_languages': '⚠️ Nu există carduri cu limbile selectate.\nAdaugă carduri sau modifică setările de limbă',
        'total_cards': 'Total {} carduri'
    }
} 

# Промты для GPT на разных языках
GPT_PROMPTS = {
    'ru': '''Ты - помощник для изучения языков. Сгенерируй 10 часто используемых слов из категории "Еда и напитки".

Требования к ответу:
1. Строго придерживайся формата ниже
2. Не добавляй никаких пояснений или дополнительного текста
3. Ответ должен быть обёрнут в три обратные кавычки

Формат:
🇷🇺: [Cлово] | 🇬🇧: [Word] | 🇪🇸: [Palabra] | 🇷🇴: [Cuvânt]''',

    'en': '''You are a language learning assistant. Generate 10 commonly used words from the "Food and Drinks" category.

Requirements for the response:
1. Strictly follow the format below
2. Do not add any explanations or additional text
3. The response must be wrapped in triple backticks

Format:
🇷🇺: [Cлово] | 🇬🇧: [Word] | 🇪🇸: [Palabra] | 🇷🇴: [Cuvânt]''',

    'es': '''Eres un asistente de aprendizaje de idiomas. Genera 10 palabras comunes de la categoría "Comida y Bebidas".

Requisitos para la respuesta:
1. Sigue estrictamente el formato a continuación
2. No agregues explicaciones ni texto adicional
3. La respuesta debe estar envuelta en comillas invertidas triples

Formato:
🇷🇺: [Cлово] | 🇬🇧: [Word] | 🇪🇸: [Palabra] | 🇷🇴: [Cuvânt]''',

    'ro': '''Ești un asistent pentru învățarea limbilor. Generează 10 cuvinte frecvent utilizate din categoria "Mâncare și Băuturi".

Cerințe pentru răspuns:
1. Urmează strict formatul de mai jos
2. Nu adăuga explicații sau text suplimentar
3. Răspunsul trebuie să fie încadrat în ghilimele triple inverse

Format:
🇷🇺: [Cлово] | 🇬🇧: [Word] | 🇪🇸: [Palabra] | 🇷🇴: [Cuvânt]'''
} 