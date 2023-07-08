# Image styling telegram bot

Я выполнял проект по курсу Deep Learning School от МФТИ по созданию телеграм-бота, который переносит стиль с одного изображения на другое при помощи MSG-Net - нейросети основанной на GAN'ах. При выполнении проекта удалось написать полностью функционирующего бота, обернуть его в докер и сделать деплой на сервере (хоть и с ограничениями на память). 

Бот: @image_styling_tg_bot  
На настоящий момент бот уже отключён, просто в силу ограниченности ресурса сервера (читай раздел "3. Докер и деплой")

Касательно репозитория: 
1. В директории "notebook" есть, соответственно, ноутбук и папка "test" - они предназначены для демонстрации работы нейросети (остальное смотрите ниже). 
2. Для запуска бота по своему API и на своём железе скачайте **всю директорию "tgbot", app.py, и API.txt**.  
**!** В API.txt впишите токен, который вам выдаст @BotFather. Запуск бота происходит через app.py. Все необходимые библиотеки указаны в requirements.txt.
3. Для запуска через Docker ещё необходимо скачать Dockerfile. Подробнее про работу с докером в разделе "3. Докер и деплой"

Ниже приведены комментарии о выборе нейросети, деталях пользования ботом, о деплое бота (с докером) и, наконец, небольшая демонстрация результатов.

## 1. Выбор сетки для бота
Была выбрана нейросеть MSG-Net в реализации от zhanghang1989 [1].  
**MSG-Net имеет следующие преимущества** перед другими аналогами (CycleGan или Deep Photo Style Transfer) в задаче переноса стиля с одного изображения на другое:
  1. Нейросеть имеет достаточно хорошее качество переноса стиля.
  2. Реализация понятна и лаконична, что позволяет без особых усилий использовать msg-net.
  3. И самое главное - MSGNet не такая ресурсоёкая, как та же Deep Photo Style Transfer, что, как следствие, даёт относительно быструю скорость обработки изображений и позволяет задеплоить сеть на бесплатных ресурсах.

**Однако есть и недостатки**: по сравнению с Deep Photo Style Transfer качество результирующего переноса может быть посредственным. Например, вы могли загрузить фотку кота как исходное изображение и фото звёздного неба, как стиль - на выходе может не получиться звёздный кот. Полагаю, это из-за того, что архитектура MSG-Net, хоть и удобная, но не такая глубокая как у её конкурента (у Deep Photo Style Transfer используются фичи нейросети VGG-19, что очевидно и даёт сильно повышенное качество). Поэтому результат переноса стиля может не всегда соответствовать ожиданиям (последний сет картинок в разделе "5. Результаты").  

Далее речь пойдёт о файлах из папки "notebook".  
Примеры переноса стиля можно посмотреть в файле "final-project-net-and-examples.ipynb", также в ноутбуке присутствует раздел для интересующихся, где можно попробовать перенести стиль одного изображения на другое. Всё, что нужно - указать путь к соответствующим изображениям из папок "image" и "style", предназначенных для изображений и стилей для них, соответственно.

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
4. В боте указана команда /tests. Она не влияет на работу бота и предназначена лишь для демонстрации картинок при разных значениях параметра image_size (при обработке изображений). В телеграме лучше всего заметна разница при перелистывании фотографий - поэтому решил выделить для этого отдельную команду.
5. У бота есть ограничение - не реализован многопользовательский режим, так как это не являлось основной задачей. Бот рассчитан лишь на одного пользователя. Если 2 или более юзера будут одновременно пользоваться ботом, оригинальное изображение и изображение стиля будут перезаписываться и результат будет представлять собой обработку последних двух загруженных фотографий. Таким образом, все пользователи получат какой-то один непредсказуемый для них результат.


Для повышения скорости работы MSG-Net и стабильности сервера был выбран image_size равный 512*512 пикселей. Однако, если есть желание увеличить качество изображений - измените значение image_size в коде, в файле "tgbot.py". Оно находится в начале функции result. Просто помните, что это увеличит потребление памяти и, как следствие, задержку вывода в боте. Лучше всего делать подобные эксперименты на своём железе, если позволяют ресурсы, либо - если нет, то можно воспользоваться платформой kaggle, залить туда вышеупомянутый ноутбук "final-project-net-and-examples.ipynb" и в нём поменять image_size на тот, что вас интересует - ресурсов точно должно хватить.  

Источники:  
[1] https://docs.aiogram.dev/en/latest/  
[2] https://mastergroosha.github.io/aiogram-3-guide/  

## 3. Докер и деплой
Создание докер-образа и его последующее размещение на сервере реализовано на ПО Docker [1]. Давайте поближе посмотрим на процесс развёртывания сервера:

1. Сначала скачиваем Docker Desktop для вашей операционной системы [2]. **Начиная с пункта 3**, приложение **должно** быть запущено. 
2. Для проекта пишем 2 файла: с зависимостями вашего бота - requirements.txt, и непосредственно сам Dockerfile со всеми необходимыми командами. Последний можно написать в VSCode, установив расширение "Docker" от Microsoft. [3]
![image](https://github.com/tipofyzik/ImageStyling_tgbot/assets/84290230/f74565bf-d25c-4dc4-866c-aa56df11ca37)  
3. В консоли переходим в директорию, где находится ваш проект и Dockerfile. Затем пишем следующую команду:  
**docker build -t your_image_name path_to_dockerfile**  
После ввода команды начнётся процесс сборки docker-образа. После завершения сборки вы сможете протестировать работу образа, запустив его при помощи команды:  
**docker run your_image_name**  
5. Далее нас интересует выгрузка docker-образа. Заходим на docker-hub [4], проходим регистрацию и входим в аккаунт. Возвращаемся в нашу консоль и пишем **docker login** для входа в аккаунт, далее пишем следующие команды:  
**docker tag your_image_name dockerhub_username/your_image_name**  
**docker push dockerhub_username/your_image_name**  
Первая строчка создаёт новое имя для нашего образа - это нужно для загрузки на docker-hub, которая происходит после введения второй строчки. По завершении загрузки, Desktop Docker, как и консоль нам больше не потребуются.

Теперь всё, что нужно - docker playground [5] - сайт от docker.com, позволяющий запускать хоть и ограниченную по памяти (4GB), но бесплатную 4х часовую сессию. На наше счастье, предоставленных ресурсов достаточно для работы бота. Заходим на сайт, выбираем Lab Environment:  
![image](https://github.com/tipofyzik/ImageStyling_tgbot/assets/84290230/13d41a2e-242a-4031-b4c6-7d32a7c29718)  
Логинимся, нажимаем "start". Теперь нам нужно лишь нажать "add new instance" и ввести команду:  
**docker run -it dockerhub_username/your_image_name**  
После чего наш образ c docker hub загрузится и бот запустится.

your_image_name - имя вашего докер-образа  
dockerhub_username - ник в docker hub  
path_to_dockerfile - путь к папке, где лежит Dockerfile  

В силу всего вышесказанного, можно понять, что бота постоянно поддерживать тяжело в силу ограничений по времени и памяти. Поэтому он отключён

**!Замечание:**  
Когда пишете Dockerfile и файл с зависимостями проекта, очень рекомендую устанавливать лишь самый минимум, необходимый для работы бота (да и проекта в целом).  Например, если в requirements.txt вы просто укажете версию для библиотеки torch, то в образ будет скачиваться довольно большой пакет, в котором, в частности, будет находится функционал для работы с GPU, который для работы проекта вообще не нужен. В данном случае лучше поставить версию torch лишь для CPU, это существенно снизит размер скачиваемого пакета. По этой же причине поставлен лишь базовый образ Python и почищен весь кэш. Благодаря подобному решению, финальный размер образа удалось уменьшить с исходных 7.5ГБ до примерно 1ГБ, что очень хорошо в условиях ограниченных бесплатных ресурсов.  

Источники:  
[1] https://ru.wikipedia.org/wiki/Docker  
[2] https://www.docker.com/  
[3] https://code.visualstudio.com/docs/containers/overview  
[4] https://hub.docker.com/  
[5] https://www.docker.com/play-with-docker/  

## 4. Условности
Теперь об особенностях пользования:  
1. Так как ресурсы сервера ограничены, рекомендую не закидывать очень тяжёлые фотографии. Это, как минимум, просто увеличит время обработки, как максимум, сервер умрёт и придётся перезапускать.
2. Как я и говорил ранее, для увеличения скорости отчати бота на сервере в tgbot.py размер изображение выставлен 512*512 пикселей. Увеличение размера, также вешает сервер при обработке файлов.
Я в своих экспериментах с ботом (на сервере) загружал изображения около 5Мб каждое - ответ получался. Однако если увеличить image_size до 1024, то с теми же самыми фотографиями сервер умирал, видимо, из-за ресурсоёмкости обработки. Если хочется увидеть качество получше - читай последний абзац раздела "2. Телеграм бот".

## 5. Результаты
И напоследок несколько результатов, сгенерированных ботом)    
![image](https://github.com/tipofyzik/ImageStyling_tgbot/assets/84290230/43092759-6ba8-495e-9619-17966e5cdebc)  
![image](https://github.com/tipofyzik/ImageStyling_tgbot/assets/84290230/b3fe0a1c-8fdb-4317-800e-5c111e5b0bc7)  
![image](https://github.com/tipofyzik/ImageStyling_tgbot/assets/84290230/107eefd3-bb2b-4d4b-85cc-b92375701c87)  

