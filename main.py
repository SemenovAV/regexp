import csv
import re

with open("phonebook_raw.csv", encoding='utf8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    result = {}
    name_patern = re.compile('(^[А-ЯЁ][а-яё]*)\s?\,?(([А-Я][а-яё]*)\s?\,?([А-Я][а-яё]*)?)\,?$')
    name_sub_patern = r'\1,\3,\4,'
    key_sub_patern = r'\1,\3'
    phone_patern = re.compile('(\+7|8)\s?\(?(495|812)\)?\-?\s?(\d{3})\-?(\d{2})\-?(\d{2})(\s?\(?(доб.)\s?(\d+)\)?)?')
    phone_sub_patern = r'+7(\2)\3-\4-\5 \7\8'
    keys = contacts_list[0]

    for item in contacts_list[1:]:
        name = name_patern.sub(name_sub_patern, ''.join(item[:2])).split(',')
        item[0] = name[0]
        item[1] = name[1]
        item[2] = name[2]
        item[5] = phone_patern.sub(phone_sub_patern, item[5])
        key = (item[1], item[0])
        data = result.setdefault(key, {
        })
        count = 0
        for elem in keys:
            data[elem] = data.get(elem) or item[count]
            result[key] = data
            count += 1
    with open("phonebook.csv", "w", encoding='utf8') as result_f:
        datawriter = csv.writer(result_f, delimiter=',', lineterminator='\n')
        datawriter.writerows([keys])
        datawriter.writerows(elem.values() for elem in result.values())
