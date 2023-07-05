# Image styling telegram bot

1. В основной директории есть ноутбук и папка "test" - он для демонстрации работы нейросети (осталньое смотрите ниже). 
2. Для запуска бота по своему API и на своём железе скачайте **всю директорию "tgbot"**.  
  2.1. Если хотите запустить через докер, не забудьте скачать **Dockerfile** и **requirements.txt** и положить их в одно место **вместе** с папкой tgbot.  
Запуск бота на компьютере происходит при помощи файла **"app.py"**. В файле **"tgbot.py"** не забудьте указать свой API token.

Ниже приведены комментарии касательно выбора нейросети, процесса создания бота и деталей его использования и, наконец, небольшая демонстрация результатов.

## 1. Выбор сетки для бота
Была выбрана нейросеть MSG-Net в реализации от zhanghang1989 [1].
MSG-Net имеет следующие преимущества перед другими аналогами (CycleGan или Deep Photo Style Transfer) в задаче переноса стиля с одного изображения на другое:
  1. Нейросеть имеет достаточно хорошее качество переноса стиля
  2. Реализация достаточно понятна и лаконична, что позволяет без особых усилий использовать msg-net

Примеры переноса стиля можно посмотреть в файле "final-project-net-and-examples.ipynb", также в нотубуке присутствует раздел для интересующихся, где можно попробовать перенести стиль одного изображения на другое. Всё, что нужно - указать путь к соответствующим изображениям из папок "image" и "style", предназначенных для изображений и стилей для них, соответственно.

Код не был изменён, за исключением исправления одной функции - tensor_load_rgbimage(...), так как вылезала ошибка при её вызове. Проблема возникала при изменении размера изображения, а именно, в параметре Image.ANTIALIAS из библиотеки Pillow - он устарел и был удалён 1 июля 2023. 
![image](https://github.com/tipofyzik/ImageStyling_tgbot/assets/84290230/11452491-057f-4251-97f6-c6f3804ccda6)
По этой причине используется Image.LANCZOS, результат применения которого едва ли уступает предыдущему методу.  
Также был подправлен ввод и вывод тестовых изображений, однако это никак не повлияло на сеть и функции обработки изображений и данное изменение сделано лишь для удобства проведения тестов.  

MSG-Net:     
[1] https://github.com/zhanghang1989/PyTorch-Multi-Style-Transfer     
[2] https://www.researchgate.net/figure/An-overview-of-MSG-Net-Multi-style-Generative-Network-The-transformation-network_fig1_315489372

## 2. Телеграм бот
Бот создан при помощи @BotFather. Библиотека, используемая для работы с ним - aiogram. Все зависимости указаны в "requirements.txt"

Отмечу пару моментов касательно работы бота:
1. Для загрузки новых фотографий совсем не обязательно нажимать /restart.  Можно просто выбрать тип фотографии при помощи соответствующей команды и загрузить её. Этой опция доступна всегда!
2. Фотографии будут присваиваться тому типу, который вы выбрали в последний раз и этот тип не измениться, пока вы сами его не поменяете при помощи команды.
3. Каждому типу присваивается лишь последняя фотография - остальные не будут никак учитываться при получении результата.
4. В боте указана команда /tests. Она не влияет на работу бота и предназначена лишь для демонстрации картинок при значениях параметра. В телеграме лучше всего заметна разница при перелистывании фотографий - поэтому решил выделить для этого отдельную команду.

Также, для повышения качества работы MSG-Net я изменил размер изображений при их обработке (функция transform_image) с 512 (как в ноутбуке) на 1024. Если есть желание увеличить скорость обработки и выдачи изображений - измените значение в коде. Оно находится в начале функции result. 

Источники:

## 3. Докер и деплой
