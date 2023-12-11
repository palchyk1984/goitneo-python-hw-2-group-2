
# Chagelog for bot version 0.2:
# - added error decorator
# - Версія бота перекладена на Англійску мову

# Розділення введеного рядка на команду та аргументи
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

# Декоратор для обробки помилок введення користувача
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please. Use add <name> <phone number>"
        except KeyError:
            return "Contact not found:"
        except IndexError:
            return "Invalid command format. Use: command <name> <phone>"

    return inner

# Завантаження контактів з текстового файлу
@input_error
def load_contacts(filename="contacts.txt"):
    contacts = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                name, phone = line.strip().split(":")
                contacts[name] = phone
    except FileNotFoundError:
        pass
    return contacts

# Виведення усіх контактів
@input_error
def list_contacts(contacts):
    if not isinstance(contacts, dict):
        return "Контактів не знайдено."
    elif not contacts:
        return "Контактів не знайдено."
    else:
        return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())

# Додавання контакту 
@input_error
def add_contact(args, contacts):
    if len(args) == 2:
        name, phone = args
        contacts[name] = phone
        return "Контакт додано."
    else:
        raise ValueError

# Зміна номера телефону
@input_error
def change_contact(args, contacts):
    name, new_phone = args
    if name in contacts:
        contacts[name] = new_phone
        return f"Phone number for {name} changed to {new_phone}."
    else:
        raise KeyError(name)
    
# Збереження контактів у текстовий файл   
def save_contacts(contacts, filename="contacts.txt"):
    with open(filename, "w") as file:
        for name, phone in contacts.items():
            file.write(f"{name}:{phone}\n")

# Команди бота
def main():
    contacts = load_contacts()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_contacts(contacts)
            print("Goodbye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            add_result = add_contact(args, contacts)
            print(add_result)
        elif command == "all":
            print(list_contacts(contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
