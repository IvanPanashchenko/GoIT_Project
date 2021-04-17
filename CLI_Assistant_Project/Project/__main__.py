from collections import UserList
from datetime import datetime, timedelta 
from pickle import dump, load
import re
# from tkinter import *

def log(action):

    current_time = datetime.strftime(datetime.now(), '%H:%M:%S')
    message = f'[{current_time}] {action}'

    print(message)
    with open('logs.txt', 'a') as file:
        file.write(f'{message}\n')


class BotInterface:

    def __init__(self):
        self.book = AddressBook()

    def handle(self, action):
        if action == 'add':
            name = Name(input("Name: ")).value.strip()
            phones = Phone().value
            birth = Birthday().value
            email = Email().value.strip()
            status = Status().value.strip()
            note = Note(input("Note: ")).value
            record = Record(name, phones, birth, email, status, note)
            return self.book.add(record)
        elif action == 'search':
            pattern = input('Search: ')
            print(self.book.search(pattern))
        elif action == 'edit':
            contact_name = input('Contact name: ')
            parameter = input('Which parameter to edit(name, phone, birthday, status, email, note): ').strip()
            new_value = input("New Value: ")
            return self.book.edit(contact_name, parameter, new_value)
        elif action == 'remove':
            pattern = input("Remove (contact name or phone): ")
            return self.book.remove(pattern)
        elif action == 'save':
            file_name = input("File name: ")
            return self.book.save(file_name)
        elif action == 'load':
            file_name = input("File name: ")
            return self.book.load(file_name)
        elif action == 'congratulate':
            print(self.book.congratulate())
        elif action == 'view':
            print(self.book)
        else:
            print("There is no such command!")


class AddressBook(UserList):

    def __init__(self):
        self.data = []
        self.counter = -1

    def __str__(self): 
        result = []
        for account in self.data:
            if account['birthday']:
                birth = account['birthday'].strftime("%d/%m/%Y")
            else:
                birth = '' 
            if account['phone(s)']:
                new_value = []
                for number in account['phone(s)']:
                    if number:
                        new_value.append(number)
                phone = ', '.join(new_value)
            else:
                phone = ''
            result.append("_"*50+"\n"+f"Name: {account['name']} \nPhones: {phone} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n"+"_"*50 + '\n')
        return '\n'.join(result)

    def __next__(self):
        phones = []
        self.counter += 1
        if self.data[self.counter]['birthday']:
            birth = self.data[self.counter]['birthday'].strftime("%d/%m/%Y")
        if self.counter == len(self.data):
            self.counter = -1
            raise StopIteration
        for number in self.data[self.counter]['phone(s)']:
            if number:
                phones.append(number)
        result = "_"*50+"\n"+f"Name: {self.data[self.counter]['name']} \nPhones: {', '.join(phones)} \nBirthday: {birth} \nEmail: {self.data[self.counter]['email']} \nStatus: {self.data[self.counter]['status']} \nNote: {self.data[self.counter]['note']}\n"+"_"*50
        return result

    def __iter__(self):
        return self

    def __setitem__(self, index, record):
        self.data[index] = {'name' : record.name,
                            'phone(s)' : record.phones, 
                            'birthday' : record.birthday }

    def __getitem__(self, index):
        return self.data[index]

    def add(self, record):
        account = {'name' : record.name,
                   'phone(s)' : record.phones, 
                   'birthday' : record.birthday,
                   'email' : record.email,
                   'status' : record.status,
                   'note' : record.note }
        self.data.append(account)
        log(f"Contact {record.name} has been added.")

    def save(self, file_name):
        with open(file_name+'.bin', 'wb') as file:
            dump(self.data, file)
        log("Addressbook has been saved!")

    def load(self, file_name):
        with open(file_name+'.bin', 'rb') as file:
            self.data = load(file)
        return self.data
        log("Addressbook has been loaded!")

    def search(self, pattern):
        result = ""
        for account in self.data:
            if account['birthday']:
                birth = account['birthday'].strftime("%d/%m/%Y")
            if account['name'].lower().startswith(pattern.lower()):
                    result += "_"*50+"\n"+f"Name: {account['name']} \nPhones: {', '.join(account['phone(s)'])} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n"+"_"*50
            elif birth.lower().startswith(pattern.lower()):
                    result += "_"*50+"\n"+f"Name: {account['name']} \nPhones: {', '.join(account['phone(s)'])} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n"+"_"*50
            elif account['email'].lower().startswith(pattern.lower()):
                    result += "_"*50+"\n"+f"Name: {account['name']} \nPhones: {', '.join(account['phone(s)'])} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n"+"_"*50
            elif account['status'].lower().startswith(pattern.lower()):
                    result += "_"*50+"\n"+f"Name: {account['name']} \nPhones: {', '.join(account['phone(s)'])} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n"+"_"*50
            elif account['note'].lower().startswith(pattern.lower()):
                    result += "_"*50+"\n"+f"Name: {account['name']} \nPhones: {', '.join(account['phone(s)'])} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n"+"_"*50
            for phone in account['phone(s)']:
                if phone.lower().startswith(pattern.lower()):
                    result += "_"*50+"\n"+f"Name: {account['name']} \nPhones: {', '.join(account['phone(s)'])} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n"+"_"*50
        if not result:
            print('There is no such contact in address book!')
        return result

    def edit(self, contact_name, parametr, new_value):
        names = []
        try:
            for account in self.data:
                names.append(account['name'])
                if account['name'] == contact_name:
                    if parametr == 'birthday':
                        new_value = Birthday(new_value).value
                    elif parametr == 'email':
                        new_value = Email(new_value).value
                    elif parametr == 'status':
                        new_value == Status(new_value).value
                    elif parametr == 'phone':
                        new_value = new_value.split(' ')
                        for number in new_value:
                            number = Phone(number).value
                    if parametr in account.keys():
                        account[parametr] = new_value
                    elif parametr == 'phone':
                        account['phone(s)'] = new_value
                    else:
                        raise ValueError
            if contact_name not in names:    
                raise NameError
        except ValueError:
            print('Incorrect parameter! Please provide correct parameter')
        except NameError:
            print('There is no such contact in address book!')
        else:
            log(f"Contact {contact_name} has been edited!")

    def remove(self, pattern):
        for account in self.data:
            if account['name'] == pattern:
                self.data.remove(account)
                log(f"Contact {account['name']} has been removed!")
            if pattern in account['phone(s)']:
                account['phone(s)'].remove(pattern)
                log(f"Phone number of {account['name']} has been removed!")
        
    def __get_current_week(self):
        now = datetime.now()
        current_weekday = now.weekday()
        if current_weekday < 5:
            week_start = now - timedelta(days = 2 + current_weekday)
        else:
            week_start = now - timedelta(days = current_weekday - 5)
        return [week_start.date(), week_start.date() + timedelta(days = 7)]

    def congratulate(self):
        result = []
        WEEKDAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        current_year = datetime.now().year
        congratulate = {'Monday': [],'Tuesday':[],'Wednesday':[],'Thursday':[],'Friday':[]}
        for account in self.data:
            if account['birthday']:
                new_birthday = account['birthday'].replace(year = current_year)
                birthday_weekday = new_birthday.weekday()
                if self.__get_current_week()[0] <= new_birthday.date() < self.__get_current_week()[1]:
                    if birthday_weekday < 5:
                        congratulate[WEEKDAYS[birthday_weekday]].append(account['name'])
                    else:
                        congratulate['Monday'].append(account['name'])
        for key, value in congratulate.items():
            if len(value):
                result.append(f"{key}: {' '.join(value)}")
        return '_'*50+'\n'+'\n'.join(result)+'\n'+'_'*50
        

class Record:

    def __init__(self, name, phones='', birthday='', email='', status='', note=''):

        self.birthday = birthday
        self.name = name
        self.phones = phones
        self.email = email
        self.status = status
        self.note = note
        
    def days_to_birthday (self):
        current_datetime = datetime.now()
        self.birthday = self.birthday.replace(year = current_datetime.year)
        if self.birthday >= current_datetime:
            result = self.birthday - current_datetime
        else:
            self.birthday = self.birthday.replace(year = current_datetime.year + 1)
            result = self.birthday - current_datetime
        return result.days


class Field:

    def __init__(self, value):
        self.value = value

    def __getitem__(self):
        return self.value


class Name(Field):
    pass


class Phone(Field):
    
    def __init__(self, value=''):
        while True:
            self.value = []
            if value:
                self.values = value
            else:
                self.values = input("Phone(s)(+48......... or +38..........): ")
            try:
                for number in self.values.split(' '):
                    if re.match('^\+48\d{9}$', number) or re.match('^\\+38\d{10}$', number) or number == '':
                        self.value.append(number)
                    else: 
                        raise ValueError            
            except ValueError:
                print('Incorrect phone number format! Please provide correct phone number format.')
            else:
                break


class Birthday(Field):
    
    def __init__(self, value = ''):
        while True:
            if value:
                self.value = value
            else:
                self.value = input("Birthday date(dd/mm/YYYY): ")
            try:
                if re.match('^\d{2}/\d{2}/\d{4}$', self.value):
                    self.value = datetime.strptime(self.value.strip(), "%d/%m/%Y")
                    break
                elif self.value == '':
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Incorrect date! Please provide correct date format.')


class Email(Field):

    def __init__(self, value = ''):
        while True:
            
            if value:
                self.value = value
            else:
                self.value = input("Email: ")
            try:
                if re.match('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', self.value) or self.value == '':
                    break
                else: 
                    raise ValueError
            except ValueError:
                print('Incorrect email! Please provide correct email.')


class Status(Field):

    def __init__(self, value = ''):
        while True:
            self.status_types = ['','family', 'friend', 'work']
            if value:
                self.value = value
            else:
                self.value = input("Type of Relashionship(family, friend, work): ")
            try:
                if self.value in self.status_types:
                    break
                else:
                    raise ValueError
            except ValueError:
                print('There is no such status!')


class Note(Field):
    pass


if __name__ == "__main__":

    bot = BotInterface()
    bot.book.load("auto_save")
    while True:
        action = (input("Choose wright action(add,search,edit,load,remove,save,congratulate,view): ")).strip()
        bot.handle(action)
        
        if action in ['add', 'remove', 'edit']:
            bot.book.save("auto_save")
