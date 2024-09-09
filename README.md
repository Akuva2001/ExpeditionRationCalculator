# Раскладка для экспедиций

Этот проект представляет собой приложение для планирования меню на основе продуктов, блюд и дневных норм. Приложение позволяет загружать продукты, блюда и дни из YAML-файлов, а также загружать меню и проверять их на соответствие дневным нормам.

Этот проект также является портом с Kotlin на Python данного проекта: https://gitlab.com/zimy/expedition-ration-calculator-classes. При клонировании были произведены некоторые изменения конфигурации, но основной смысл остался тем же.

## Требования

Для запуска вам необходим Python, а также менеджер пакетов, например, pip. Погуглите, как их установить в вашем случае.

## Установка

1. Клонируйте репозиторий:

```
git clone https://github.com/Akuva2001/ExpeditionRationCalculator.git
```
2. Перейдите в папку проекта:
```
cd ExpeditionRationCalculator
```

3. Установите зависимости:

```
pip install -r requirements.txt
```

## Использование

1. Запустите приложение:

```
python main.py \
 --menu menu/sample_menu.yml \
 --products products/products.yml \
 --meals meals/meals.yml \
 --days days/days.yml
```

2. Приложение выведет раскладку меню, список покупок для каждой секции меню по отдельности и список покупок для всех меню вместе.
3. Вы можете изменять как сами файлы [products.yaml](products/products.yaml)
, [meals.yaml](meals/meals.yml), [days.yaml](days/days.yml), [sample_menu.yaml](menu/sample_menu.yml), так и создавать другие. При создании других файлов, не забудьте указать к ним путь в команде запуска.
4. В качестве альтернативы вы можете открыть файл [main.ipynb](main.ipynb), он имеет такой же функционал.
5. Для вывода в файл можете воспользоваться: 
```
python main.py \
 --menu menu/sample_menu.yml \
 --products products/products.yml \
 --meals meals/meals.yml \
 --days days/days.yml \
  > "раскладка.txt"
```
6. Пример вывода можно посмотреть в файле [раскладка.txt](раскладка.txt)

## Лицензия

Этот проект лицензирован под лицензию MIT. Подробности см. в файле [LICENSE](LICENSE).

## Пример вывода

```
📗 Раскладка:
📗 Секция меню "П1 дно":
  веса дней ['740', '755', '697', '771', '701'], общий вес 21986
  ❗ Слишком много калорий: 3321, избыток 121
  ❗ Слишком мало углеводов: 226, нужно ещё 64
  ❗ Слишком много калорий: 3374, избыток 174
⚠ 3
  Меню на ночёвку 1:
    ужин:    гречка с говядиной кронидов (Гречка 480, Пряники 300, Сухари 300, Тушенка говядина Кронидов 480)
    завтрак: булгур с курятиной кронидов (Булгур 480, Козинак 240, Лук 120, Сухари 90, Тушенка говядина Кронидов 480, Халва 240)
    перекус: перекус гаврюшкин (Батончики сникерс 300, Кешью 150, Колбаса 300, Курага 300, Сухари 300, Сыр 300, Финики 300)
  Меню на ночёвку 2:
    ужин:    булгур с говядиной кронидов (Булгур 480, Печенье 210, Сухари 90, Тушенка говядина Кронидов 480, Халва 240)
    завтрак: пшено с курятиной кронидов (Козинак 300, Колбаса 300, Пшено 420, Сыр 300, Тушенка курятина Кронидов 480)
    перекус: перекус гаврюшкин (Батончики сникерс 300, Кешью 150, Колбаса 300, Курага 300, Сухари 300, Сыр 300, Финики 300)
  Меню на ночёвку 3:
    ужин:    рис с говядиной кронидов (Козинак 300, Рис 360, Тушенка говядина Кронидов 480)
    завтрак: кускус с сыром и колбасой (Кисель 90, Колбаса 480, Конфеты батончики ротФронт 180, Кускус 480, Сыр 300)
    перекус: перекус гаврюшкин (Батончики сникерс 300, Кешью 150, Колбаса 300, Курага 300, Сухари 300, Сыр 300, Финики 300)
  Меню на ночёвку 4:
    ужин:    соба с курятиной кронидов (Козинак 360, Лапша Соба Гречневая 600, Майонез 180, Пряники 360, Тушенка курятина Кронидов 480)
    завтрак: макароны с говядиной Кронидов (Козинак 300, Конфеты батончики ротФронт 300, Макароны 600, Сыр 300, Тушенка говядина Кронидов 480)
    перекус: перекус гаврюшкин (Батончики сникерс 300, Кешью 150, Колбаса 300, Курага 300, Сухари 300, Сыр 300, Финики 300)
  Меню на ночёвку 5:
    ужин:    гречка с говядиной кронидов (Гречка 480, Пряники 300, Сухари 300, Тушенка говядина Кронидов 480)
    завтрак: соба с курятиной кронидов (Козинак 360, Лапша Соба Гречневая 600, Майонез 180, Пряники 360, Тушенка курятина Кронидов 480)
    перекус: перекус гаврюшкин (Батончики сникерс 300, Кешью 150, Колбаса 300, Курага 300, Сухари 300, Сыр 300, Финики 300)

📗 Секция меню "П1 поверхность":
  веса дней ['740', '755', '697', '771', '701', '697', '771', '701'], общий вес 23334
  ❗ Слишком много калорий: 3321, избыток 121
  ❗ Слишком мало углеводов: 226, нужно ещё 64
  ❗ Слишком много калорий: 3374, избыток 174
  ❗ Слишком мало углеводов: 226, нужно ещё 64
  ❗ Слишком много калорий: 3374, избыток 174
⚠ 5
  Меню на ночёвку 1:
    ужин:    гречка с говядиной кронидов (Гречка 320, Пряники 200, Сухари 200, Тушенка говядина Кронидов 320)
    завтрак: булгур с курятиной кронидов (Булгур 320, Козинак 160, Лук 80, Сухари 60, Тушенка говядина Кронидов 320, Халва 160)
    перекус: перекус гаврюшкин (Батончики сникерс 200, Кешью 100, Колбаса 200, Курага 200, Сухари 200, Сыр 200, Финики 200)
  Меню на ночёвку 2:
    ужин:    булгур с говядиной кронидов (Булгур 320, Печенье 140, Сухари 60, Тушенка говядина Кронидов 320, Халва 160)
    завтрак: пшено с курятиной кронидов (Козинак 200, Колбаса 200, Пшено 280, Сыр 200, Тушенка курятина Кронидов 320)
    перекус: перекус гаврюшкин (Батончики сникерс 200, Кешью 100, Колбаса 200, Курага 200, Сухари 200, Сыр 200, Финики 200)
  Меню на ночёвку 3:
    ужин:    рис с говядиной кронидов (Козинак 200, Рис 240, Тушенка говядина Кронидов 320)
    завтрак: кускус с сыром и колбасой (Кисель 60, Колбаса 320, Конфеты батончики ротФронт 120, Кускус 320, Сыр 200)
    перекус: перекус гаврюшкин (Батончики сникерс 200, Кешью 100, Колбаса 200, Курага 200, Сухари 200, Сыр 200, Финики 200)
  Меню на ночёвку 4:
    ужин:    соба с курятиной кронидов (Козинак 240, Лапша Соба Гречневая 400, Майонез 120, Пряники 240, Тушенка курятина Кронидов 320)
    завтрак: макароны с говядиной Кронидов (Козинак 200, Конфеты батончики ротФронт 200, Макароны 400, Сыр 200, Тушенка говядина Кронидов 320)
    перекус: перекус гаврюшкин (Батончики сникерс 200, Кешью 100, Колбаса 200, Курага 200, Сухари 200, Сыр 200, Финики 200)
  Меню на ночёвку 5:
    ужин:    гречка с говядиной кронидов (Гречка 320, Пряники 200, Сухари 200, Тушенка говядина Кронидов 320)
    завтрак: соба с курятиной кронидов (Козинак 240, Лапша Соба Гречневая 400, Майонез 120, Пряники 240, Тушенка курятина Кронидов 320)
    перекус: перекус гаврюшкин (Батончики сникерс 200, Кешью 100, Колбаса 200, Курага 200, Сухари 200, Сыр 200, Финики 200)
  Меню на ночёвку 6:
    ужин:    рис с говядиной кронидов (Козинак 200, Рис 240, Тушенка говядина Кронидов 320)
    завтрак: кускус с сыром и колбасой (Кисель 60, Колбаса 320, Конфеты батончики ротФронт 120, Кускус 320, Сыр 200)
    перекус: перекус гаврюшкин (Батончики сникерс 200, Кешью 100, Колбаса 200, Курага 200, Сухари 200, Сыр 200, Финики 200)
  Меню на ночёвку 7:
    ужин:    соба с курятиной кронидов (Козинак 240, Лапша Соба Гречневая 400, Майонез 120, Пряники 240, Тушенка курятина Кронидов 320)
    завтрак: макароны с говядиной Кронидов (Козинак 200, Конфеты батончики ротФронт 200, Макароны 400, Сыр 200, Тушенка говядина Кронидов 320)
    перекус: перекус гаврюшкин (Батончики сникерс 200, Кешью 100, Колбаса 200, Курага 200, Сухари 200, Сыр 200, Финики 200)
  Меню на ночёвку 8:
    ужин:    гречка с говядиной кронидов (Гречка 320, Пряники 200, Сухари 200, Тушенка говядина Кронидов 320)
    завтрак: соба с курятиной кронидов (Козинак 240, Лапша Соба Гречневая 400, Майонез 120, Пряники 240, Тушенка курятина Кронидов 320)
    перекус: перекус гаврюшкин (Батончики сникерс 200, Кешью 100, Колбаса 200, Курага 200, Сухари 200, Сыр 200, Финики 200)


📘 Список покупок для каждой секции меню по отедльности:
📘 Меню: П1 дно, вес: 21986
  Крупы:
    Булгур: 1600
    Гречка: 1920
    Кускус: 1120
    Лапша Соба Гречневая: 2800
    Макароны: 1400
    Пшено: 700
    Рис: 840
  Овощи:
    Лук: 200
  Мясо и молочка:
    Колбаса: 4720
    Сыр: 5000
    Тушенка говядина Кронидов: 5760
    Тушенка курятина Кронидов: 3040
  Сладкое:
    Батончики сникерс: 3100
    Козинак: 3980
    Конфеты батончики ротФронт: 1120
    Печенье: 350
    Пряники: 2880
    Халва: 800
  Сухофрукты и орехи:
    Кешью: 1550
    Курага: 3100
    Финики: 3100
  Другое:
    Кисель: 210
    Майонез: 840
    Сухари: 4600

📘 Меню: П1 поверхность, вес: 23334
  Крупы:
    Булгур: 1600
    Гречка: 1920
    Кускус: 1120
    Лапша Соба Гречневая: 2800
    Макароны: 1400
    Пшено: 700
    Рис: 840
  Овощи:
    Лук: 200
  Мясо и молочка:
    Колбаса: 4720
    Сыр: 5000
    Тушенка говядина Кронидов: 5760
    Тушенка курятина Кронидов: 3040
  Сладкое:
    Батончики сникерс: 3100
    Козинак: 3980
    Конфеты батончики ротФронт: 1120
    Печенье: 350
    Пряники: 2880
    Халва: 800
  Сухофрукты и орехи:
    Кешью: 1550
    Курага: 3100
    Финики: 3100
  Другое:
    Кисель: 210
    Майонез: 840
    Сухари: 4600


📗📗 Список покупок для всех меню вместе:
Крупы:
  Булгур: 1600
  Гречка: 1920
  Кускус: 1120
  Лапша Соба Гречневая: 2800
  Макароны: 1400
  Пшено: 700
  Рис: 840
Овощи:
  Лук: 200
Мясо и молочка:
  Колбаса: 4720
  Сыр: 5000
  Тушенка говядина Кронидов: 5760
  Тушенка курятина Кронидов: 3040
Сладкое:
  Батончики сникерс: 3100
  Козинак: 3980
  Конфеты батончики ротФронт: 1120
  Печенье: 350
  Пряники: 2880
  Халва: 800
Сухофрукты и орехи:
  Кешью: 1550
  Курага: 3100
  Финики: 3100
Другое:
  Кисель: 210
  Майонез: 840
  Сухари: 4600
Общий вес: 45320

```