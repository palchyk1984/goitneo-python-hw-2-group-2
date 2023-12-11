# Chagelog for bot version 0.4:
# - added new classes for 
# - - class CommandParser
# - - class ErrorHandler
# - - class FileManager:
# - - class ContactManager:

# Classes
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number format should be max 10 digits")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name}, phones: {', '.join(map(str, self.phones))}"


class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def load_contacts(self, filename="contacts.txt"):
        try:
            with open(filename, "r") as file:
                for line in file:
                    name, phones_str = line.strip().split(":")
                    phones = phones_str.split(";")
                    record = Record(name)
                    for phone in phones:
                        record.add_phone(phone)
                    self.add_record(record)
        except FileNotFoundError:
            pass

    def save_contacts(self, filename="contacts.txt"):
        with open(filename, "w") as file:
            for record in self.data.values():
                file.write(f"{record.name.value}:{';'.join(map(str, record.phones))}\n")


class CommandParser:
    @staticmethod
    def parse_input(user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, args


class ErrorHandler:
    @staticmethod
    def input_error(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError as e:
                return str(e)
            except KeyError:
                return "Contact not found."
            except IndexError:
                return "Invalid command format."

        return inner


class FileManager:
    @staticmethod
    def load_contacts(address_book, filename="contacts.txt"):
        address_book.load_contacts(filename)

    @staticmethod
    def save_contacts(address_book, filename="contacts.txt"):
        address_book.save_contacts(filename)


class ContactManager:
    @staticmethod
    def add_contact(args, address_book):
        if len(args) >= 1:
            name = args[0]
            record = Record(name)
            if len(args) == 2:
                phone = args[1]
                record.add_phone(phone)
            address_book.add_record(record)
            return "Contact added."
        else:
            raise ValueError("Give me name and phone, please. Use add <name> <phone number>")


    @staticmethod
    def delete_contact(args, address_book):
        if len(args) == 1:
            name = args[0]
            address_book.delete(name)
            return f"Contact {name} deleted."
        else:
            raise ValueError("Give me a name to delete.")

    @staticmethod
    def change_contact(args, address_book):
        if len(args) == 2:
            name, new_phone = args
            record = address_book.find(name)
            if record:
                record.edit_phone(record.phones[0].value, new_phone)
                return f"Phone number for {name} changed to {new_phone}."
            else:
                raise KeyError
        else:
            raise ValueError("Give me name and new phone, please.")
   
    @staticmethod
    def list_contacts(address_book):
        if not address_book.data or not any(address_book.data.values()):
            return "Contacts not found."
        else:
            return "\n".join(str(record) for record in address_book.data.values())
    

# Команди бота
if __name__ == "__main__":
    address_book = AddressBook()
    FileManager.load_contacts(address_book)
    print("Welcome to the assistant bot!")
    print('-' * 45 + '\nMain commands:\n'
                     'hello - greeting message\n'
                     'all - show all contacts\n'
                     'find - number search by name\n'
                     'findphone - search contacts by phone number\n'
                     'add - add new contact\\contact number\n'
                     'change - change contact number\n'
                     'addphone - add phone number to an existing contact\n'
                     'removephone - remove phone number from an existing contact\n'
                     'editphone - edit phone number for an existing contact\n'
                     'del - delete contact\\number\n' + '-' * 45)

    while True:
        user_input = input("Enter command: ")
        command, args = CommandParser.parse_input(user_input)

        if command in ["close", "exit"]:
            FileManager.save_contacts(address_book)
            print("Goodbye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(ContactManager.add_contact(args, address_book))
        elif command == "all":
            result = ContactManager.list_contacts(address_book)
            print(result)
        elif command == "change":
            print(ContactManager.change_contact(args, address_book))
        elif command == "find":
            print(ContactManager.find_contact(args, address_book))
        elif command == "del":
            print(ContactManager.delete_contact(args, address_book))
        elif command == "addphone":
            print(ContactManager.add_phone_to_contact(args, address_book))
        elif command == "removephone":
            print(ContactManager.remove_phone_from_contact(args, address_book))
        elif command == "editphone":
            print(ContactManager.edit_phone_for_contact(args, address_book))
        elif command == "findphone":
            print(ContactManager.find_by_phone(args, address_book))
        else:
            print("Invalid command.")
