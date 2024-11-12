import re
from datetime import datetime, timedelta
import subprocess

def parse_timecode(timecode):
    start_str, end_str = timecode.split(' --> ')
    start = datetime.strptime(start_str, '%H:%M:%S,%f')
    end = datetime.strptime(end_str, '%H:%M:%S,%f')
    return start, end

def generate_ffmpeg_commands(srt_file, images_folder, output_file, alpha_format='webm'):
    with open(srt_file, 'r', encoding='utf-8') as file:
        content = file.read()

    blocks = re.split(r'\n\n', content.strip())
    ffmpeg_commands = []
    index = 1
    start_times = []
    end_times = []

    # Читаем все таймкоды
    for block in blocks:
        lines = block.splitlines()
        timecode = lines[1]
        start, end = parse_timecode(timecode)
        start_times.append(start)
        end_times.append(end)

    # Общая длительность видео
    final_end_time = end_times[-1]
    total_duration = (final_end_time - start_times[0]).total_seconds()

    # Генерация команд ffmpeg с перераспределением длительности
    for i, block in enumerate(blocks):
        lines = block.splitlines()
        timecode = lines[1]
        start, end = parse_timecode(timecode)

        # Длительность текущего кадра
        duration = (end - start).total_seconds()

        # Если между текущим и следующим кадром есть пауза, то увеличиваем длительность текущего кадра
        if i + 1 < len(blocks):
            next_start, _ = parse_timecode(blocks[i + 1].splitlines()[1])
            pause_duration = (next_start - end).total_seconds()
            if pause_duration > 0:
                duration += pause_duration  # Добавляем паузу к текущему кадру

        image_file = f"{images_folder}/image_{index}.png"
        ffmpeg_commands.append(f"file '{image_file}'\nduration {duration:.3f}\n")
        index += 1

    # Добавляем финальный кадр
    if ffmpeg_commands:
        ffmpeg_commands.append(f"file '{image_file}'\n")

    # Записываем команды в файл
    with open('ffmpeg_commands.txt', 'w') as f:
        f.write(''.join(ffmpeg_commands))

    # Выбираем параметры кодека для webm с альфа-каналом
    if alpha_format == 'webm':
        output_codec = 'libvpx-vp9 -pix_fmt yuva420p -auto-alt-ref 0 -crf 25 -b:v 0'
        output_extension = 'webm'
    else:
        raise ValueError("Unsupported format. Only 'webm' is supported.")

    ffmpeg_command = f"ffmpeg -f concat -safe 0 -i ffmpeg_commands.txt -c:v {output_codec} {output_file}.{output_extension}"
    subprocess.run(ffmpeg_command, shell=True)

# Запуск функции
generate_ffmpeg_commands('subtitles_output.srt', './images', 'output_video', alpha_format='webm')
