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
            return "Give me name and phone please."
        except KeyError as e:
            return f"Contact not found: {e}"
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



# Оновлення функції add_contact з декоратором input_error
@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."

# Оновлення функції change_contact з декоратором input_error
@input_error
def change_contact(args, contacts):
    name, new_phone = args
    if name in contacts:
        contacts[name] = new_phone
        return f"Phone number for {name} changed to {new_phone}."
    else:
        raise KeyError(name)

# Оновлення функції main для використання декоратора input_error
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
            print(add_contact(args, contacts))
        elif command == "all":
            print(list_contacts(contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
