#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# Конфигурация путей (можно менять)
BASE_DIR = os.path.expanduser("~/message_templates")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
RECIPIENTS_FILE = os.path.join(BASE_DIR, "recipients.txt")
AUTHORS_FILE = os.path.join(BASE_DIR, "authors.txt")
INFO_OPTIONS_FILE = os.path.join(BASE_DIR, "info_options.txt")

def ensure_dir_exists(dirpath):
    """Создает директорию если ее не существует"""
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

def load_file_contents(filepath):
    """Загружает содержимое файла или возвращает None если файла нет"""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def save_to_file(filepath, content):
    """Сохраняет содержимое в файл"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def load_templates():
    """Загрузка шаблонов из файловой структуры"""
    try:
        # Создаем базовую структуру, если ее нет
        ensure_dir_exists(BASE_DIR)
        ensure_dir_exists(TEMPLATES_DIR)
        
        # Создаем примеры файлов при первом запуске
        if not os.path.exists(RECIPIENTS_FILE):
            save_to_file(RECIPIENTS_FILE, "Алексей Петров|менеджер по продажам\nМария Сидорова|директор по маркетингу")
        
        if not os.path.exists(AUTHORS_FILE):
            save_to_file(AUTHORS_FILE, "ООО 'Технологии'|sales@tech.ru\nИП Сергеев|info@sergeev.ru")
        
        if not os.path.exists(INFO_OPTIONS_FILE):
            save_to_file(INFO_OPTIONS_FILE, "Заказ готов|ваш заказ готов к выдаче\nПодписание|договор требует подписания")
        
        # Создаем папки с шаблонами
        for category in ["greetings", "main_parts", "endings"]:
            category_dir = os.path.join(TEMPLATES_DIR, category)
            ensure_dir_exists(category_dir)
            
            # Создаем примеры шаблонов
            if not os.listdir(category_dir):
                if category == "greetings":
                    save_to_file(os.path.join(category_dir, "01_Официальное.txt"), "Уважаемый(ая) {name}!")
                    save_to_file(os.path.join(category_dir, "02_Стандартное.txt"), "Добрый день, {name}!")
                elif category == "main_parts":
                    save_to_file(os.path.join(category_dir, "01_Нейтральное.txt"), "Сообщаем вам, что {info}.")
                    save_to_file(os.path.join(category_dir, "02_Радостное.txt"), "Мы рады сообщить вам, что {info}!")
                elif category == "endings":
                    save_to_file(os.path.join(category_dir, "01_Формальное.txt"), "С уважением, {author}.")
                    save_to_file(os.path.join(category_dir, "02_С_контактами.txt"), "Будем рады вашим вопросам!\n{contacts}")

        # Загружаем данные
        def load_pairs(filepath):
            pairs = {}
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        if '|' in line:
                            key, value = line.strip().split('|', 1)
                            pairs[key] = value
            return pairs

        data = {
            "recipients": load_pairs(RECIPIENTS_FILE),
            "authors": load_pairs(AUTHORS_FILE),
            "info_options": load_pairs(INFO_OPTIONS_FILE)
        }

        # Загружаем шаблоны
        templates = {}
        for category in ["greetings", "main_parts", "endings"]:
            category_dir = os.path.join(TEMPLATES_DIR, category)
            templates[category] = {}
            
            for filename in sorted(os.listdir(category_dir)):
                if filename.endswith('.txt'):
                    name = os.path.splitext(filename)[0].split('_', 1)[1]
                    filepath = os.path.join(category_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        templates[category][name] = f.read()

        return data, templates

    except Exception as e:
        print(f"Ошибка загрузки шаблонов: {e}")
        raise

def select_from_files(title, items):
    """Выбор из загруженных данных с нумерацией"""
    print(f"\n{title}:")
    keys = list(items.keys())
    for i, key in enumerate(keys, 1):
        print(f"{i}. {key}")
    
    while True:
        try:
            choice = int(input("Ваш выбор (номер): ")) - 1
            if 0 <= choice < len(keys):
                return keys[choice], items[keys[choice]]
            print("Ошибка: введите номер из списка!")
        except ValueError:
            print("Ошибка: введите число!")

def main():
    try:
        data, templates = load_templates()
        
        print("="*50)
        print("ГЕНЕРАТОР ТЕКСТА (шаблоны в файлах)")
        print("="*50)

        # Выбор получателя
        recipient, position = select_from_files("Выберите получателя", data["recipients"])
        
        # Выбор отправителя
        author, contacts = select_from_files("Выберите отправителя", data["authors"])
        
        # Выбор информации
        info_title, info_text = select_from_files("Выберите тип сообщения", data["info_options"])
        
        # Выбор шаблонов
        greeting_name, greeting = select_from_files("Выберите приветствие", templates["greetings"])
        main_part_name, main_part = select_from_files("Выберите основную часть", templates["main_parts"])
        ending_name, ending = select_from_files("Выберите заключение", templates["endings"])

        # Формирование текста
        context = {
            "name": recipient,
            "info": info_text,
            "author": author,
            "contacts": contacts
        }

        final_text = (
            greeting.format(**context) + "\n\n" +
            main_part.format(**context) + "\n\n" +
            ending.format(**context)
        )

        # Вывод и сохранение
        print("\n" + "="*50)
        print(f"СООБЩЕНИЕ ДЛЯ: {recipient} ({position})")
        print(f"ТИП: {info_title}")
        print(f"СТИЛЬ: {greeting_name} / {main_part_name} / {ending_name}")
        print("="*50)
        print(final_text)
        print("="*50)

        # Сохранение
        output_dir = os.path.join(BASE_DIR, "output")
        os.makedirs(output_dir, exist_ok=True)
        filename = f"message_{recipient.split()[0]}_{info_title.replace(' ', '_')}.txt"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_text)
        
        print(f"\nСохранено в: {filepath}")

    except Exception as e:
        print(f"\nОшибка: {e}")
    finally:
        input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()
