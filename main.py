import random
import os
from time import sleep
from download import download
folder_name = 'modules'
directory = f".\\{folder_name}\\"

# Чтение файла со списком слов
def read_file_data(filename: str):
    words_dict= dict()
    if filename:
        with open(f"{folder_name}\\{filename}", 'r', encoding='utf-8') as file:
            try:
                for line in file:
                    key, value = line.split(':', 1)  # Извлекаем ключ и значение
                    words_dict[key] = value.rstrip(';')
            except FileNotFoundError as e:
                print(f"Файл не найден в директории {folder_name}\\{filename}.\n{str(e)}")
                return -1
    return words_dict

# С русского на английский
def rus_to_eng(words_dict, test_type='отработка', sleeptime=0.5):
    true_answers, false_answers = 0, 0
    while words_dict:
        answer, question = random.choice(list(words_dict.items()))
        print(print(question.split(',')[0]))
        user_input = str(input(": ")).strip()

        if user_input == answer:
            print("Верный перевод!")
            true_answers += 1
            words_dict[answer] = question[question.find(',') + 1:]
            if not words_dict[answer]:
                words_dict.pop(answer)
        else:
            print(f"Неверный перевод!\nИстинна: {answer}")
            if test_type == 'проверка':
                false_answers += 1
                words_dict[answer] = question[question.find(',') + 1:]
                if not words_dict[answer]:
                    words_dict.pop(answer)
            sleep(sleeptime)
        os.system("cls")
        print(f"Верных: {true_answers}\nНеверных: {false_answers}\n")
    return 0

# С английского на русский
def eng_to_rus(words_dict, test_type='отработка', sleeptime=0.5):
    true_answers, false_answers = 0, 0
    while words_dict:
        question, answer = random.choice(list(words_dict.items()))
        print(question)
        correct_words = [word.strip() for word in answer.split(',') if word.strip()]
        user_input = str(input(": ")).strip()
        if user_input in correct_words:
            true_answers += 1
            correct_words.remove(user_input)
            words_dict[question] = ','.join(correct_words) + ',' if correct_words else None
            if words_dict[question] is None:
                words_dict.pop(question)
        else:
            print(f"Неверный перевод!\nИстинна: {answer[:-1]}")
            if test_type == 'проверка':
                false_answers += 1
                words_dict[question] = ','.join(correct_words) + ',' if correct_words else None
                if words_dict[question] is None:
                    words_dict.pop(question)
            sleep(sleeptime)
        os.system("cls")
        print(f"Верных: {true_answers}\nНеверных: {false_answers}\n")
    return 0

def before_start_test(test_type):
    while True:
        try:
            print("0. Назад\n1. Отработка\n2. Проверка")
            menu_input = input(": ")[0]
            if menu_input == '0':
                break

            print("Выберите модуль:\n0. Назад")
            list_dir = os.listdir(directory)
            for i, module in enumerate(list_dir, 1):
                print(f"{i}. {module}")
            module = int(input(": ")) - 1
            sleep_time = int(input("Время перед исчезновением в секундах(0-9)\n: "))
            if menu_input == "1":
                if test_type == "etr":
                    eng_to_rus(read_file_data(list_dir[module]), 'отработка', sleep_time)
                else:
                    rus_to_eng(read_file_data(list_dir[module]), 'отработка', sleep_time)
                break
            elif menu_input == "2":
                if test_type == "rte":
                    rus_to_eng(read_file_data(list_dir[module]), 'проверка', sleep_time)
                else:
                    eng_to_rus(read_file_data(list_dir[module]), 'проверка', sleep_time)
                break
        except (IndexError, ValueError):
            print("Введите корректное значение в поле ввода.")

def menu(foldername):
    if os.path.isdir(foldername):
        while True:
            try:
                print("0. Выход\n1. С англ на русс\n2. С русс на англ")
                menu_input = input(": ")
                if menu_input == "0":
                    break
                elif menu_input == "1":
                    before_start_test('etr')
                elif menu_input == "2":
                    before_start_test("rte")
                else:
                    print("Введите корректное значение.")
            except KeyboardInterrupt:
                break
    else:
        print("Не найдено папки с модулями.\nВы можете скачать авторские нажав 1\nДля выхода введите что-то кроме 1")
        download_input = input(': ')[0]
        if download_input == "1":
            os.system("cls")
            if not download():
                return False
        return True

if __name__ == "__main__":
    while True:
        if not menu(folder_name):
            break