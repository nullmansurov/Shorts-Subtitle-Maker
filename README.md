Это приложение предназначен что бы быстро создать динамичные субтитры для шортса. Поскольку субтитры дает динамичность и помагает удерживать внимание, это очень полезный инструмент.

Сначала вам необходимо получить транскрипцию вашего видео и субтитры в формате srt. Можете в ручную это сделать через Aegisub или другие прилоежение или можете использовать автоматизированный вариант от меня. Whisper OpenAI большая языковая модель. Она хорошо создает транскрипцию

⭐ **Создать субтитры через Whisper** [![Open in Colab](https://raw.githubusercontent.com/hollowstrawberry/kohya-colab/main/assets/colab-badge.svg)]([https://colab.research.google.com/github/hollowstrawberry/kohya-colab/blob/main/Lora_Trainer.ipynb](https://colab.research.google.com/github/nullmansurov/Shorts-Subtitle-Maker/blob/main/whisper_subtitles.ipynb))

Потом вам необходимо на ваш компьютер установить ffmpeg. Как это сделать найдете в интернете

После полученного subtitle.srt скидывайте в директорию проекта. 
Потом запускаем **start_edit_subs.bat**. Скрипт подготовить субтитры для работы остальной части кода
После запускаем **start.bat**. Это открывает для вас GUI, где вы можете настроить стиль скрипта. (Цвет текста, размер текста, расположение текста, фон текста) и нажимает **Создать субтитры**
Подождите пока не получите ответ что субтитры успешно созданы

Запускаем **start_create_video.bat**. В этот раз открывается терминал. Вам ничего не надо делать, просто немного подождите.
После получите в этой же директории видео **output_video.webm**
Видео будет в формате webm и с альфа каналом. Вам необходимо просто в видеоредакторе скинуть сверху вашего видео поулченный медифайл. Можете немного замедлить видео, поставить где-то 0.9 или 0.75х, потому что иногда субтитры могут слишком сильно спешит

После запускайте **start_cleaner.bat** - она удаляет служебные файлы, что бы потом сразу можно было по новому создавать субтитры

P.s: не советвую использовать для создания видео с большими хронометражами. И только для 9:16 формате, поскольку в скрипте изначально так указан. Или можете сами в ручную указать в коде и превратить в горизантольный формат. Однока, нагрузка на комп если слишком большой видео, будет большим
