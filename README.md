# GLRParser

Анонс в блоге: http://vas3k.ru/blog/358/

Инструмент извлечения структурированных данных (фактов) из текста на естественном (русском) языке на Python 2.x. Построен с использованием любимого всеми морфологического анализатора pymorphy2 и никому неизвестного GLR-парсера jupyLR (был взят как самый простой для переписывания). Чем-то похож на Томита-парсер Яндекса (http://api.yandex.ru/tomita/), хотя чего греха таить, общем-то проект и был начат из-за сложной применимости Томита-парсера простыми смертными в силу особеностей его распространения и небогатой документации. По которой, в прочем, вполне очевидно, что сам парсер был открыт Яндексом лишь частично, а цель помочь простым смертным при этом была далеко не на первом месте (иначе бы Яндекс распространял его не скудным бинарником, а оформил как остальные свои проекты в библиотеку или демон).

Проект практически повторяет открытую функциональность Томита-парсера, однако написан на чистом python и открыт, что позволяет использовать его в реальных проектах и модифицировать. А еще не болен протобафом головного мозга, а использует понятные и простые питонячие структуры данных. Возможно когда-нибудь Яндекс таки дооткроет Томита-парсер и настанут светлые времена, а пока таким вот отщепенцам как я приходится выживать как могут.

Подробнее про работу GLR-парсеров и алгоритма Томиты можно почитать на википедии или нагуглить. http://ru.wikipedia.org/wiki/GLR-%D0%BF%D0%B0%D1%80%D1%81%D0%B5%D1%80

Для примера можно смотреть example.py.

```
from glr import GLRParser

dictionaries = {
    u"CLOTHES": [u"куртка", u"пальто", u"шубы"]
}

grammar = u"""
    S = adj<agr-gnc=1> CLOTHES
"""

glr = GLRParser(grammar, dictionaries=dictionaries)

text = u"на вешалке висят три красивые куртки и вонючая шуба"
for parsed in glr.parse(text):
    print parsed

# вернет ["красивые куртки", "вонючая шуба"]

```

## Примерное описание работы

1. Входной текст разбивается на предложения по символам [!?;\.]+, а так же очищается от лишних символов. Если такое поведение не устраивает, модифицируйте splitter.py.
2. Каждое предложение разбивается на токены согласно регулярным выражениям в glr.py (константа DEFAULT_PARSER). Модифицируя этот список, можно вводить свои терминальные символы в грамматику (токены новых типов, например, можно ввести отдельный тип для чисел).
3. Каждый токен нормализуется и к нему добавляются его морфологические характеристики. Морфологическая неоднозначность снимается... никак. Берется просто первая форма, которую вернул pymorphy2. Если такое поведение не устраивает - милости прошу в normalizer.py и в пулл реквесты.
4. Дальше стандартный GLR-парсинг входной строки. Если строка не разбирается, то отбрасывается первый токен и все повторяется заново. Все совпадения откладываются и в конце возвращается список.

## Синтаксис грамматик

**Начальный символ** — S (можно менять параметром root в конструкторе GLRParser);

**Нетерминал** - зарезервированное слово в нижнем регистре (adj, verb, noun, см. начало GLRParser чтобы научиться вводить свои);

**Терминал** — слово с большой буквы (зарезервированное Word или любое введенное прям в грамматике AsYouWish);

**Словари** - слово капсом, означающее название словаря (например CITIES), сами словари задаются как { "CITIES": ["val1", "val2", ...]} и передаются в конструктор GLRParser;

**Одно слово** - слово в 'одинарных' 'кавычках', будет искаться во всех своих формах (например 'шуба') (hint: в грамматике слово нужно указывать в начальной форме, а то не найдется);

**Лейблы** - список через запятую в &lt;угловых скобочках&gt; после терминала/нетерминала.

```
S = SomeClothes
SomeClothes = adj 'шуба'
SomeClothes = adj 'валенок'
```

## Словари

Словарь задается простым питоновским словарем (каламбурчик). Ключи - названия словарей, их принято писать капсом. А еще лучше везде использовать юникод-строки, а то мало ли. Например:

```
dictionaries = {
    u"НАЗВАНИЕ_СЛОВАРЯ": [u"значение1", u"значение2", ...]
}
```

Пример использования есть выше.

## Список зарезервированных терминалов и нетерминалов

| Символ  | Значение                 |
| ------- | ------------------------ |
| Word    | Любое слово              |
| noun    | Существительное          |
| adj     | Прилагательное           |
| verb    | Глагол                   |
| pr      | Причастие                |
| dpr     | Деепричастие             |
| num     | Числительное (или число) |
| adv     | Наречие                  |
| pnoun   | Местоимение              |
| prep    | Предлог                  |
| conj    | Союз                     |
| prcl    | Частица                  |
| lat     | Слово на латинице        |


## Список лейблов

Лейблами можно задавать ограничения или сочетаемость слов. Заметьте, что лейблы могут сильно повлиять на производительность, если применять их к слишком широким по значению (не)терминалам. Не увлекайтесь. Лейблы всегда проверяются только на этапе свертки, если вы понимаете о чем я.


| Символ        | Значение                                                                                                                                  |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| gram          | Слово имеет какое-то грамматическое свойство, например определенный падеж. Пример: adj&lt;gram=gent&gt; — прилагательное в родительном падеже.  |
| reg-l-all     | Все буквы в слове нижнего регистра. Пример: noun&lt;reg-l-all&gt; - существительное, все буквы маленькие.                                       |
| reg-h-first   | Первая буква - заглавная. Пример: noun&lt;reg-h-first&gt; - существительное с заглавной буквы.                                                  |
| reg-h-all     | Все буквы заглавные (капс). Пример аналогичен предыдущим.                                                                                 |
| agr-gnc       | Согласование по роду, числу, падежу (gender, number, case). Пример: adj&lt;arg-gnc=1&gt; noun - прилагательное согласуется со следующим за ним существительным по роду, числу, падежу. Обратите внимание, цифра указывает с каким по счету словом от этого сравнивать (возможно и отрицательное значение).|
| agr-nc        | По числу и падежу (number, case). Пример аналогичен.                                                                                      |
| agr-c         | По падежу (case).                                                                                                                         |
| agr-gn        | По роду и числу (gender, number).                                                                                                         |
| agr-gc        | По роду и падежу (gender, case).                                                                                                          |
| regex         | Слово удовлетворяет регулярному выражению. Пример: word&lt;regex=[0-9]+&gt;.                                                                    |


Можно указывать сразу по нескольку лейблов через запятую. Например noun&lt;reg-l-all, gram=nomn&gt; — существительное в именительном падеже, все буквы которого в нижнем регистре.

Список грамматических категорий см. в доке pymorphy2: https://pymorphy2.readthedocs.org/en/latest/user/grammemes.html