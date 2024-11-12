import os
import shutil

def cleanup_files_and_folder():
    # Удаляем файлы, если они существуют
    files_to_delete = ['ffmpeg_commands.txt', 'subtitles_output.srt', 'subtitles.srt', 'text.txt']
    for file in files_to_delete:
        if os.path.isfile(file):
            os.remove(file)
            print(f"Удален файл: {file}")
        else:
            print(f"Файл не найден: {file}")

    # Удаляем папку images, если она существует
    folder_to_delete = 'images'
    if os.path.isdir(folder_to_delete):
        shutil.rmtree(folder_to_delete)
        print(f"Удалена папка: {folder_to_delete}")
    else:
        print(f"Папка не найдена: {folder_to_delete}")

# Запуск функции очистки
cleanup_files_and_folder()
