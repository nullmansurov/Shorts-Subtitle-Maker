import re
from datetime import datetime, timedelta

def split_text_into_segments(text, max_words=5):
    words = text.split()
    segments = []
    segment = []
    word_count = 0

    for word in words:
        if word_count < max_words:
            segment.append(word)
            word_count += 1
        else:
            segments.append(' '.join(segment))
            segment = [word]
            word_count = 1

    if segment:
        segments.append(' '.join(segment))

    return segments

def parse_timecode(timecode):
    start_str, end_str = timecode.split(' --> ')
    start = datetime.strptime(start_str, '%H:%M:%S,%f')
    end = datetime.strptime(end_str, '%H:%M:%S,%f')
    return start, end

def format_timecode(time):
    return time.strftime('%H:%M:%S,%f')[:-3]

def distribute_time(start, end, segment_lengths):
    total_words = sum(segment_lengths)
    total_duration = (end - start).total_seconds()
    time_ranges = []
    current_time = start

    for length in segment_lengths:
        segment_duration = total_duration * (length / total_words)
        segment_end = current_time + timedelta(seconds=segment_duration)
        time_ranges.append((current_time, segment_end))
        current_time = segment_end

    return time_ranges

def process_subtitles(input_file, output_text_file, output_srt_file, max_words=5):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    blocks = re.split(r'\n\n', content.strip())
    processed_text = []
    processed_srt = []
    index = 1

    for block in blocks:
        lines = block.splitlines()
        subtitle_index = lines[0]
        timecode = lines[1]
        text = ' '.join(lines[2:])

        segments = split_text_into_segments(text, max_words)
        processed_text.extend(segments)

        start, end = parse_timecode(timecode)

        # Calculate segment lengths and distribute time accordingly
        segment_lengths = [len(segment.split()) for segment in segments]
        time_ranges = distribute_time(start, end, segment_lengths)

        for i, segment in enumerate(segments):
            start_time, end_time = time_ranges[i]
            formatted_timecode = f"{format_timecode(start_time)} --> {format_timecode(end_time)}"
            processed_srt.append(f"{index}\n{formatted_timecode}\n{segment}\n")
            index += 1

    with open(output_text_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(processed_text))

    with open(output_srt_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(processed_srt))

# Запуск функции
process_subtitles('subtitles.srt', 'text.txt', 'subtitles_output.srt', max_words=5)
