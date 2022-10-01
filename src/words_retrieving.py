import re
from string import digits



def check_capitalized_words(content, pronouns, particula):
    cyrillic_letters = r'\b[А-Я]\w*'
    latin_letters = r'\b[A-Z]\w*'
    capital_words =  re.findall(latin_letters, raw_content) + re.findall(cyrillic_letters, raw_content)
    cap_unique = list()
    for i in capital_words:
        if len(i) < 2 or i.lower() in pronouns or i.lower() in particula:
            continue ;
        if i not in cap_uniquecap_unique:
            cap_unique.append(i)
    with open('caps_to_check.txt', 'w') as file:
        for i in cap_unique:
            file.write(i + "\n")
    return cap_unique
         

def delete_parenthesis(content):
    with open('parenthesis.txt', 'r') as f:
        parenthesis = f.read().split(', ')
    drop_parenthesis = [i for i in content.split(', ') if i.lower() not in parenthesis]
    drop_parenthesis = ", ".join(drop_parenthesis).replace('-', ' ')
    return drop_parenthesis


def delete_sings_digits(content):
    punc = '''!()-[]{};:"\,<>./?@#$%^&*_~'''
    for ele in content:
        if ele in punc:
            content = content.replace(ele, "")
    table = str.maketrans('', '', digits)
    content = content.translate(table)
    filtered_words = [i for i in content.split(" ") if i != '']
    return content

def create_corpus(content, pronouns, particula):
    with open('Capitalized.txt', 'r') as file:
        capitalized = file.read().split('\n')
    filtered_words = [i for i in content.split(" ") if i != '']
    corpus = list()
    for i in filtered_words:
        if i.lower() in pronouns or i.lower() in particula or i in capitalized:
            continue ;
        else:
            corpus.append(i.lower())
    return list(set(corpus))


def get_book_corpus(name):    
    book = open(name, 'r')
    content = book.read()
    with open('pronouns.txt', 'r') as f:
        pronouns = f.read().replace('\n', ' ').split(', ')
    with open('particula.txt', 'r') as f:
        particula = f.read().split(', ')    
#     check_capitalized_words(content, pronouns, particula)    
    raw_content = delete_parenthesis(" ".join(content.split()))
    raw_content = delete_sings_digits(raw_content)
    corpus = create_corpus(raw_content, pronouns, particula)
    return corpus


    
if __name__ == "__main__":
#     name = '../books/Intermezzo.txt'
    books = ['../books/Intermezzo.txt',
             '../books/Климко.txt',
             '../books/Місто.txt',
             '../books/Захар_Беркут.txt',
             '../books/Кобзар.txt',
             '../books/Тигролови.txt',
             '../books/Земля.txt',
             '../books/Лісова_пісня.txt',
             '../books/Тіні_забутих_предків.txt',
             '../books/Зів\'яле_листя.txt',
             '../books/Мартин_Боруля.txt',
             '../books/Хіба_ревуть_воли_як_ясла_повні.txt',
             '../books/Кайдашева_сім\'я.txt',
             '../books/Маруся_Чурай.txt',
             '../books/Чорна_Рада.txt',
             '../books/Камінний_хрест.txt',
             '../books/Мина_Мазайло.txt',
             '../books/Я_романтика.txt']
    vocabulary = list()
    for i in books:
        vocabulary += get_book_corpus(i)
        vocabulary = list(set(vocabulary))
    with open('corpus.txt', 'w') as file:
        for i in vocabulary:
            file.write(i + "\n")
    