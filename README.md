# ukrainian_words
Dataset of Ukrainian literary words

## Description
In this repository, I started a huge process of processing the Ukrainian literary language in order to simplify its use in further projects that may include the Ukrainian language.
Some of the most popular works of Ukrainian literature were used as raw data.

## Books to be processed
- [ ] Кобзар
- [ ] Лісова пісня
- [ ] Ворошиловград
- [ ] Маруся Чурай
- [ ] Тореадори з Васюківки
- [ ] Камінний хрест
- [ ] Житіє гаремноє
- [ ] Зів‘яле листя
- [ ] Тигролови
- [ ] Я (романтика)
- [ ] Місто
- [ ] Тіні забутих предків
- [ ] Земля
- [ ] Захар Беркут
- [ ] Інтермеццо
- [ ] Мино Мазайло
- [ ] Чорна Рада
- [ ] Хіба ревуть воли як ясла повні
- [ ] Кайдашева сім‘я
- [ ] Мартин Боруля
- [ ] Гімн демократичної молоді


| Book | Format |
| ---- | ------ |
|Кобзар| txt |
|Лісова пісня| txt |
|Ворошиловград||
|Маруся Чурай| txt |
|Тореадори з Васюківки||
|Камінний хрест| txt |
|Житіє гаремноє||
|Зів‘яле листя| txt |
|Тигролови| txt |
|Я (романтика)| txt |
|Місто| txt |
|Тіні забутих предків| txt |
|Земля| txt |
|Захар Беркут| txt |
|Intermezzo| txt |
|Мино Мазайло| txt |
|Чорна Рада| txt |
|Хіба ревуть воли як ясла повні| txt |
|Кайдашева сім‘я| txt |
|Мартин Боруля| txt |
|Гімн демократичної молоді||


## Stages of processing

1. Retrieving data
- [ ] retrieve raw text from the books in different formats;
- [ ] cut texts into sentences;
- [ ] delete numbers and dates;
- [ ] get list of all words starting with capital letter;
- [ ] filter the list;
- [ ] split sentences into words dealing correctly with apostrophes;
- [ ] lowercase all the words;
- [ ] create corpus;

2. Preprocessing

- [ ] lematization;
- [ ] stemming;
- [ ] create corpus;
- [ ] create a vocabulary of stop-words;
- [ ] TF-IDF counting;
- [ ] Word2Vec;
- [ ] GloVe;

3. Exploratory Data Analysis

- [ ] words maps;
- [ ] check lenghts and frequencies;
- [ ] find most used words;

4. Create a voiced dataset of most used words

5. Create GAN model to generate text (optional)
