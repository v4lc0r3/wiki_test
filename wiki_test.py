import requests
from bs4 import BeautifulSoup as BS4


r = requests.get('https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2').text
#print(r)

soup = BS4(r, "html.parser")

# Поиск ликнов на флаги
pic = []
covers = soup.select('table.wikitable a.image img[src]')
for cover in covers:
    pic.append(cover['src'])
    # print(cover['src'])
# print(covers)
# print(pic)

# Поиск коротк. и полн. названий стран по таблице - поиск 1
my_table = soup.find('table', class_='wikitable')
items = my_table.findAll('td')

# print(items)
# print(len(items))

all_countries = []
# Формируем список всего содержимого из поиска 1
for i in range(len(items)):
    items[i] = items[i].text.strip('\n')  # удаление появившегося символа переноса
    all_countries.append(items[i])
# print(all_countries)

countries_short = []
countries_full = []


# Формируем списки полн. и коротк. назв. стран
for j in range(3, (len(items)), 4):
    countries_full.append(all_countries[j])
    countries_short.append(all_countries[j-1])
# print(countries_short)
# print(countries_full)

# Кол-во слов в полном названии
sum_of_words = []
for word in countries_full:
    space_count = 1 # сразу установим знач. 1
    for char in word:
        if char == ' ':
            space_count += 1
    sum_of_words.append(space_count)
    #print(f"{word}, количество слов: {space_count}")

# Кол-во стран на ту же букву
same_letter = []
for word in countries_short:
    same_count = 0
    for words in countries_short:
        if word[0] == words[0]:
            same_count += 1
    same_letter.append(same_count)
    #print(f"{word}, количество слов с такой буквы: {same_count}")

# Формируем список словарей
catalog = []
key_list = ["country", "full_name", "same_letter_count", "sum_words_full_name", "flag_url"]

for i in range(len(countries_short)):
    catalog.append({key_list[0]: countries_short[i],key_list[1] : countries_full[i], key_list[2] : same_letter[i], key_list[3] : sum_of_words[i], key_list[4] : pic[i]})

#print(catalog)

# Функция поиска страны
def search_country(text):
    search_text = text.lower().strip() # примодим вводимую фразу к нижн. регистру, удаляем пробелы
    # воспользуемся существующим списком и соответствующим списком словарей
    for i in range(len(countries_short)):
        if countries_short[i].lower() == search_text: # регистронезависимое сравнение
            result = (catalog[i])
            break                                     # значения уникальны, сразу останавливаем цикл при совпадении
        else:
            result = "Такой страны в списке нет. Введите другое название"
    return print(result)

# Интерактивный бесконечн. цикл запросов с вызовом фукции поиска
while True:
    text = input("Введите название страны : ")
    search_country(text)