def read_people(file):  # Читаем файл, проверяем данные и преобразуем в список словарей
    people = []
    errors = []

    try:
        with open(file, encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                parts = line.split(', ')

                if len(parts) != 11:  # проверка на наличие всех полей в строке
                    errors.append(f"Строка {line_num}: ожидается 11 полей, получено {len(parts)}")
                    continue

                try:  # преобразование входных данных
                    surname = parts[0].strip()
                    name = parts[1].strip()
                    patronymic = parts[2].strip()
                    street = parts[3].strip()
                    house = int(parts[4])
                    apartment = int(parts[5])
                    floor = int(parts[6])
                    com_space = float(parts[7])
                    liv_space = float(parts[8])
                    count_of_people = int(parts[9])
                    privilege_str = parts[10].strip().lower()

                    if privilege_str not in ['true', 'false']:
                        errors.append(f"Строка {line_num}: некорректное значение льготы '{parts[10]}'")
                        continue

                    privilege = privilege_str == 'true'

                    # Проверка входных данных
                    error_messages = []

                    if house <= 0:
                        error_messages.append(f"номер дома ({house})")

                    if apartment <= 0:
                        error_messages.append(f"номер квартиры ({apartment})")

                    if com_space <= 0:
                        error_messages.append(f"общая площадь ({com_space})")

                    if liv_space <= 0:
                        error_messages.append(f"жилая площадь ({liv_space})")

                    if liv_space > com_space:
                        error_messages.append(f"жилая площадь ({liv_space}) больше общей ({com_space})")

                    if count_of_people <= 0:
                        error_messages.append(f"количество жильцов ({count_of_people})")

                    if count_of_people == 0 and privilege:
                        error_messages.append("льгота без прописанных жильцов")

                    if error_messages:
                        errors.append(f"Строка {line_num}: некорректные значения - " + ", ".join(error_messages))
                        continue

                    if not surname or any(char.isdigit() for char in surname):
                        errors.append(f"Строка {line_num}: некорректная фамилия '{surname}'")
                        continue

                    if not name or any(char.isdigit() for char in name):
                        errors.append(f"Строка {line_num}: некорректное имя '{name}'")
                        continue

                    if not patronymic or any(char.isdigit() for char in patronymic):
                        errors.append(f"Строка {line_num}: некорректное отчество '{patronymic}'")
                        continue

                    if not street or street.isdigit():
                        errors.append(f"Строка {line_num}: некорректная улица '{street}'")
                        continue

                    # Добавляем запись о жильце в словарь
                    person = {
                        "surname": surname,
                        "name": name,
                        "patronymic": patronymic,
                        "street": street,
                        "house": house,
                        "apartment": apartment,
                        "floor": floor,
                        "com_space": com_space,
                        "liv_space": liv_space,
                        "count_of_people": count_of_people,
                        "privilege": privilege
                    }
                    people.append(person)

                except ValueError as e:
                    errors.append(f"Строка {line_num}: ошибка преобразования - {e}")
                    continue
                except Exception as e:
                    errors.append(f"Строка {line_num}: неожиданная ошибка - {e}")
                    continue

    except FileNotFoundError:
        print(f"Файл '{file}' не найден")
        return [], ["Файл не найден"]
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return [], ["Ошибка чтения файла"]

    return people, errors


def show_read_result(people, errors, total_lines=0):  # вывод информации о прочитанном файле
    if errors:
        print("\n" + "="*100)
        print("НАЙДЕНЫ ОШИБКИ В ПРЕДОСТАВЛЕННЫХ ДАННЫХ:")
        print("="*100)
        for i, error in enumerate(errors, 1):
            print(f"! {i:3}. {error}")
        print("="*100)
        print(f"Всего ошибок: {len(errors)}")

    if people:
        if total_lines > 0:
            print(f"\n Успешно прочитано {len(people)} записей из {total_lines}")
        else:
            print(f"\n Успешно прочитано: {len(people)} корректных записей")
        print("\n" + "=" * 100)
        print("ПРИМЕР ЗАПИСИ:")
        print("=" * 100)

        show_records(people[:1])

        if len(people) > 1:
            count = len(people) - 1
            if count % 10 == 1 and count % 100 != 11:
                word = "запись"
            else:
                if count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
                    word = "записи"
                else:
                    word = "записей"
            print(f"... и еще {count} {word}")

    return len(people) > 0


def show_records(records, start=0, count=None):  # вывод словорей в читаемом виде
    if not records:
        print("  (нет записей)")
        return
    records_to_show = records
    if count is not None and count > 0:
        records_to_show = records[:count]

    for i, person in enumerate(records_to_show, start=start + 1):
        privilege_text = "есть" if person["privilege"] else "нет"
        print(f"{i}. {person['surname']} {person['name']} {person['patronymic']}")
        print(f"   Адрес: ул.{person['street']}, д.{person['house']}, кв.{person['apartment']}, "
              f"эт.{person['floor']}")
        print(f"   Площадь: общая: {person['com_space']} кв.м., жилая: {person['liv_space']} кв.м.")
        print(f"   Прописано: {person['count_of_people']} чел., Льгота: {privilege_text}\n")


def ask(errors_flag):  # Вопрос о продолжении работы после проверки файла
    if not errors_flag:
        return True

    print("\n" + "="*100)
    print("Что делаем дальше?")
    print("="*100)
    print("1 - Продолжить работу с корректными данными")
    print("2 - Закрыть программу (для исправления файла)")
    print("="*100)

    while True:
        choice = input().strip()
        if choice == "1":
            return True
        elif choice == "2":
            print("\n Программа закрыта. Исправьте файл и запустите снова.")
            return False
        else:
            print("Пожалуйста, введите 1 или 2")


def shell_sort(arr, key=None, reverse=False): # Сортировка Шелла с возможностью указать ключи для комплексной сортировки
    if key is None:
        key = lambda x: x

    gap = len(arr) // 2

    while gap > 0:
        for i in range(gap, len(arr)):
            curr = arr[i]
            curr_key = key(curr)
            pos = i

            while pos >= gap:
                temp = arr[pos - gap]
                temp_key = key(temp)

                if reverse:
                    swap = temp_key < curr_key
                else:
                    swap = temp_key > curr_key

                if swap:
                    arr[pos] = arr[pos - gap]
                    pos -= gap
                else:
                    break

            arr[pos] = curr
        gap //= 2
    return arr


def task1(people):  # Функция для создания первого отчета
    sorted_people = shell_sort(
        people.copy(),
        key=lambda p: (
            -p["count_of_people"],
            p["street"].lower(),
            p["house"],
            p["apartment"]
        )
    )
    return sorted_people


def task2(people):  # Функция для создания второго отчета
    privilege_people = [p for p in people if p["privilege"]]

    sorted_people = shell_sort(
        privilege_people.copy(),
        key=lambda p: (
            p["floor"],
            -p["count_of_people"],
            p["com_space"]
        )
    )
    return sorted_people


def task3(people, n1, n2):  # функция для создания третьего отчета
    filtered_people = [p for p in people if n1 <= p["com_space"] <= n2]

    sorted_people = shell_sort(
        filtered_people.copy(),
        key=lambda p: (
            0 if p["privilege"] else 1,
            -p["com_space"]
        )
    )
    return sorted_people
