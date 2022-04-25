import re
import csv

PHONE_PATTERN = '(\+7|8)?\s*?\(?(\d{3})\)?(-|\s*)?(\d{3})(-|\s)*(\d{2})(-|\s)*(\d{2})([^,])?\s?\(?([а-я.]+)?\s?(\d{4})?\)?'
PHONE_FORMAT = r'+7(\2)\4-\6-\8 \10\11'

def getting_data():
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list

def contact_list(contacts_list):
    """Создание списка контактов и приведение его в один формат"""
    new_contact_list = list()
    for contact in contacts_list:
        contact_name = ",".join(contact[:3])
        trim_name = re.findall(r'(\w+)', contact_name)
        if len(trim_name) < 3:
            trim_name.append('')
        new_contact = [trim_name[0], trim_name[1], trim_name[2], contact[3], contact[4].capitalize(),
                       re.sub(PHONE_PATTERN, PHONE_FORMAT, contact[5]), contact[6]]
        new_contact_list.append(new_contact)
    return new_contact_list


def format_contact(contact_list):
    """Форматирование списка контактов (проверка контакта по имени и фамилии, удаление дупликатов)"""
    phone_book = dict()
    for contact in contact_list:
        key_contact = f'{contact[0]} {contact[1]}'
        if key_contact in phone_book:
            value_contact = phone_book[key_contact]
            for i in range(len(value_contact)):
                if contact[i]:
                    value_contact[i] = contact[i]
        else:
            phone_book[key_contact] = contact
    return list(phone_book.values())

def output_data(format_contact_list):
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(format_contact_list)

if __name__ == '__main__':
    contact_list_noformat = getting_data()
    new_list = contact_list(contact_list_noformat)
    contact_list_format = format_contact(new_list)
    output_data(contact_list_format)
