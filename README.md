# Image styling telegram bot

## 1. Выбор сетки для бота
Была выбрана нейросеть MSG-Net в реализации от zhanghang1989.
MSG-Net имеет следующие преимущества перед другими аналогами (CycleGan или Deep Photo Style Transfer) в задаче переноса стиля с одного изображения на другое:
  1. Нейросеть имеет достаточно хорошее качество переноса стиля
  2. Реализация достаточно понятна и лаконична, что позволяет без особых усилий использовать msg-net

Примеры переноса стиля можно посмотреть в файле "final-project-net-and-examples.ipynb", также в нотубуке присутствует раздел для интересующихся, где можно попробовать перенести стиль одного изображения на другое. Всё, что нужно - указать путь к соответствующим изображениям из папок "image" и "style", предназначенных для изображений и стилей для них, соответственно.

Файл "MSGNet.py" содержит в себе первые 2 пункта из ноутбука с примерами - архитектуру сети и функции для работы с изображениями. Это сделано для удобства работы c ботом.

Код был исправлен лишь в одном функции - tensor_load_rgbimage(...), так как вылезала ошибка при её вызове. Проблема возникала при изменении размера изображения, а именно, в параметре Image.ANTIALIAS из библиотеки Pillow - он устарел и был удалён 1 июля 2023. 
![image](https://github.com/tipofyzik/ImageStyling_tgbot/assets/84290230/11452491-057f-4251-97f6-c6f3804ccda6)
По этой причине используется Image.LANCZOS, результат применения которого едва ли уступает предыдущему методу.

Также был подправлен ввод и вывод тестовых изображений, однако это никак не повлияло на сеть и функции обработки изображений и данное изменение сделано лишь для удобства проведения тестов.


MSG-Net:  https://github.com/zhanghang1989/PyTorch-Multi-Style-Transfer

## 2. Телеграм бот
Бот создан при помощи @BotFather. Библиотека, используемая для работы с ним - aiogram.

Отмечу пару моментов:
1. Для загрузки новых фотографий совсем не обязательно нажимать /restart. 
Можно просто выбрать тип фотографии при помощи соответствующей команды и загрузить её. 
Этой опцией можно пользоваться всегда!
2. Фотографии будут присваиваться тому типу, который вы выбрали в последний раз и этот тип не измениться, пока вы сами его не поменяете при помощи команды.
3. Каждому типу присваивается лишь последняя фотография - остальные не будут никак учитываться при получении результата.


В конце раздела будут указаны источники, благодаря я разобрался в необходимом API библиотеки и смог реализовать всё необходимое.
