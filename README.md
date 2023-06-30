# Image styling telegram bot

## 1. Выбор сетки для бота
Была выбрана нейросеть MSG-Net в реализации от zhanghang1989.
MSG-Net имеет следующие преимущества перед другими аналогами (CycleGan или Deep Photo Style Transfer) в задаче переноса стиля с одного изображения на другое:
  1. Нейросеть имеет достаточно хорошее качество переноса стиля
  2. Реализация достаточно понятна и лаконична, что позволяет без особых усилий использовать msg-net

Примеры переноса стиля можно посмотреть в файле "final-project-net-and-examples.ipynb", также есть раздел для интересующихся, где попробовать перенести стиль одного изображения на другое. Всё, что нужно - указать путь к соответствующим изображениям из папок "image" и "style", предназначенных для изображений и стилей для них, соответственно.

Код в данной генеративной модели я не менял, за исключением ошибки, вылезавшей при вызове функции tensor_load_rgbimage(...). Проблема возникала при изменении размера изображения, а именно, в параметре Image.ANTIALIAS из библиотеки Pillow - параметр устарел и его удалили 1 июля 2023. 
![image](https://github.com/tipofyzik/ImageStyling_tgbot/assets/84290230/11452491-057f-4251-97f6-c6f3804ccda6)
По этой причине используется Image.LANCZOS, результат применения которого как минимум не уступает предыдущему методу.


MSG-Net:  https://github.com/zhanghang1989/PyTorch-Multi-Style-Transfer
