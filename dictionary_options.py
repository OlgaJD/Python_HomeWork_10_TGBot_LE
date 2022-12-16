import json

def get_count_words(dictionary):
    with open(dictionary, 'r', encoding='utf-8') as file:
        content_dict = json.load(file)
        return str(len(content_dict))


def get_words_in_process(dictionary):
    with open(dictionary, 'r', encoding='utf-8') as file:  
        content_dict = json.load(file)
        wordslist = []
        for key in content_dict.keys():
            wordslist.append(key)
        wordslist.sort()
        words = ', '.join(wordslist)
        return words


def get_transslate(word): 
    with open('learning.json', 'r', encoding='utf-8') as filel:
        learning_content = json.load(filel)
        with open('done.json', 'r', encoding='utf-8') as filed:
            done_content = json.load(filed)
            learning_content.update(done_content)
            if word.lower().replace(" ","") not in learning_content:
                return 'Ошибка'
            else:
                return learning_content[word.lower().replace(" ","")]['translation']


def get_synonym(word):   
    with open('learning.json', 'r', encoding='utf-8') as file:
        learning_content = json.load(file)
        with open('done.json', 'r', encoding='utf-8') as filed:
            done_content = json.load(filed)
            learning_content.update(done_content)
            translte = learning_content[word.lower().replace(" ","")]['synonyms']
            synonym = ', '.join(translte)            
            return synonym


def add_word(usermessage):
    if usermessage in ("Перевести", "Добавить новое слово", "Переместить в изученное", "Прогресс", "Удалить слово"):
        return 'Некорректный ввод'
    else:
        new_record = usermessage.lower().replace(" ","").split(',')
        key = new_record[0]
        with open('learning.json', 'r', encoding='utf-8') as fr:
            learning_content = json.load(fr)
            learning_content[key]={'translation':new_record[1], 'synonyms':new_record[2:] }
            with open('learning.json', 'w', encoding='utf-8') as fw: 
                fw.write(json.dumps(learning_content, ensure_ascii=False)) 
                return 'Добавлено новое слово'


def replace_word(word): 
    with open('learning.json', 'r', encoding='utf-8') as file:
        learning_content = json.load(file)
        for k, v in learning_content.items():
            if k == word.lower():                
                res = (f'{k}, {v["translation"]}, {v["synonyms"]}').replace("[",'').replace("]",'').replace("'",'').replace(" ",'')
                new_record = res.split(',')
                key = new_record[0]
                with open('done.json', 'r', encoding='utf-8') as fr:
                    done_content = json.load(fr)
                    done_content[key]={'translation':new_record[1], 'synonyms':new_record[2:] }
                    with open('done.json', 'w', encoding='utf-8') as fw: 
                        fw.write(json.dumps(done_content, ensure_ascii=False))         
        del learning_content[word]
        with open('learning.json', 'w', encoding='utf-8') as filew:
            filew.write(json.dumps(learning_content, ensure_ascii=False))
            return 'Плюс одно выученное слово! Супер'


def delete_word(word):
    with open('learning.json', 'r', encoding='utf-8') as file:
        learning_content = json.load(file)
        if word.lower().replace(" ","") not in learning_content:
            return 'Такого слова нет в вашем словаре'
        else:
            del learning_content[word.lower().replace(" ","")]
            with open('learning.json', 'w', encoding='utf-8') as filew:
                filew.write(json.dumps(learning_content, ensure_ascii=False))
                return 'Слово удалено'



def get_record(word):  ## Не используется в боте, получение элемента
    with open('learning.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for k, v in data.items():
            if k == word.lower():
                res = (f'{k}, {v["translation"]}, {v["synonyms"]}').replace("[",'').replace("]",'').replace("'",'').replace(" ",'')
                print(res, type(res))


# Загрузка примеров в словари. 

# ex_1 = {'appliance': {'translation': 'устройство', 'synonyms': ['прибор', 'приспособление']},
#         'occur': {'translation': 'происходить', 'synonyms': ['иметь место', 'встречаться', 'случаться', 'являться', 'попадаться', 'приходить на ум', 'бывать']},
#         'application': {'translation': 'приложение', 'synonyms': ['заявление', 'применение']},
#         'environment': {'translation': 'окружение', 'synonyms': ['среда']},
#         'maintain': {'translation': 'поддерживать', 'synonyms': ['сохранять', 'содержать']}        
# }

# ex_2 = {'go': {'translation': 'идти', 'synonyms': ['ехать', 'ходить, ездить']},
#         'replace': {'translation': 'заменять', 'synonyms': ['замещать', 'вернуть', 'возмещать']},
#         'respond': {'translation': 'отвечать', 'synonyms': ['реагировать', 'отзываться', 'отклик']}
# }

# def save(ex, d): # сохранить в json
#     with open(d, 'w', encoding='utf-8') as fh:  # открываем файл на запись
#         fh.write(json.dumps(ex, ensure_ascii=False))  # преобразовываем словарь data в unicode-строку и записываем в файл
#     print('БД успешно сохранена')


# ex = ex_1
# d = 'learning.json'
# ex = ex_2
# d = 'done.json'
# save(ex, d)