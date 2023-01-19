# ukrainian_words
Dataset of Ukrainian literary words

## Description

In this repository, I started a huge process of processing the Ukrainian literary language in order to simplify its use in further projects that may include the Ukrainian language.
Some of the most popular works of Ukrainian writers were used as raw data.

## Books to be processed

- [x] Кобзар
- [x] Лісова пісня
- [x] Маруся Чурай
- [x] Камінний хрест
- [x] Зів‘яле листя
- [x] Тигролови
- [x] Я (романтика)
- [x] Місто
- [x] Тіні забутих предків
- [x] Земля
- [x] Захар Беркут
- [x] Інтермеццо
- [x] Мино Мазайло
- [x] Чорна Рада
- [x] Хіба ревуть воли як ясла повні
- [x] Кайдашева сім‘я
- [x] Мартин Боруля

## Stages of processing

1. Retrieving data
- [x] retrieve raw text from the books in different formats;
- [x] cut texts into sentences;
- [x] delete numbers and dates;
- [x] get list of all words starting with capital letter;
- [x] filter the list;
- [x] split sentences into words dealing correctly with apostrophes;
- [x] lowercase all the words;
- [x] create corpus.

2. Preprocessing
- [x] lematization;
- [x] stemming;
- [x] create corpus;
- [x] create a vocabulary of stop-words;
- [x] TF-IDF counting;
- [x] tokenization;
- [ ] Word2Vec;
- [ ] GloVe.

3. Exploratory Data Analysis
- [ ] words maps;
- [x] check lenghts and frequencies;
- [x] find most used words.

4. Implement several informational search approaches
- [x] Suffix tree;
- [x] K-gram index;
- [x] Permuterm index;
- [x] Boolean search;
- [x] Two-word indexing;
- [x] SPIMI.

### Stemmers

| Stemmer Name | Authors | Year | Licence| Link |
| :---: | :---: | :---: | :---: | :---: |
| vgrichina | Vladimir Grichina | 2013 | MIT licence | [Python](https://github.com/vgrichina/ukrainian-stemmer) |
| tochytskyi | Andrii Glybovets, Volodymyr Tochytskyi | 2016 |  | [Python](https://github.com/tochytskyi/ukrstemmer) |
| tree-stem | Andrii Makukha | 2020 | BSD 2-Clause licence | [Python](https://github.com/amakukha/stemmers_ukrainian/blob/master/src/tree_stem.py) | 
