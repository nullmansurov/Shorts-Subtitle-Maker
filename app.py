import tkinter as tk
from tkinter import colorchooser, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

# Параметры изображения
width, height = 1280, 1920

# Функция для создания изображения с текстом и корректным центрированием
def create_image(text, font_size, text_color, bg_color, position, border_radius, text_pos=None):
    image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # Используем встроенный шрифт или Arial для масштабирования текста
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Подгонка шрифта для текста
    max_text_width = int(0.8 * width)  # Ограничиваем ширину текста до 80% ширины изображения
    while True:
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

        if text_width <= max_text_width or font_size < 10:
            break
        font_size -= 1
        font = ImageFont.truetype("arial.ttf", font_size)

    # Позиция текста и бокса
    box_padding = 20  # Отступы вокруг текста в боксе
    box_width = text_width + 2 * box_padding
    box_height = text_height + 2 * box_padding

    if text_pos:
        # Центрирование текста относительно заданной позиции
        x = text_pos[0] - box_width / 2
        y = text_pos[1] - box_height / 2
    else:
        if position == "center":
            x = (width - box_width) / 2
            y = (height - box_height) / 2
        elif position == "top":
            x = (width - box_width) / 2
            y = 50
        elif position == "bottom":
            x = (width - box_width) / 2
            y = height - box_height - 50
        else:
            x = (width - box_width) / 2
            y = (height - box_height) / 2

    # Рисуем фон текста с округлением
    draw.rounded_rectangle(
        [(x, y), (x + box_width, y + box_height)],
        fill=bg_color, radius=border_radius
    )

    # Рисуем текст по центру бокса
    text_x = x + (box_width - text_width) / 2
    text_y = y + (box_height - text_height) / 2
    draw.text((text_x, text_y), text, font=font, fill=text_color)

    return image

# Обновление предпросмотра
def update_preview(*args):
    text = preview_text.get()
    img = create_image(
        text=text,
        font_size=int(font_size.get()),
        text_color=text_color.get(),
        bg_color=bg_color.get(),
        position=position.get(),
        border_radius=int(border_radius.get()),
        text_pos=text_position.get()
    )
    preview_img = ImageTk.PhotoImage(img.resize((320, 480)))
    preview_label.config(image=preview_img)
    preview_label.image = preview_img

# Функция для выбора цвета текста
def choose_text_color():
    color_code = colorchooser.askcolor(title="Выберите цвет текста")[1]
    text_color.set(color_code)
    update_preview()

# Функция для выбора цвета фона
def choose_bg_color():
    color_code = colorchooser.askcolor(title="Выберите цвет фона бокса")[1]
    bg_color.set(color_code)
    update_preview()

# Функция для создания изображений из текстового файла
def create_images():
    with open("text.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    output_dir = "images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for idx, line in enumerate(lines):
        line = line.strip()
        if line:
            img = create_image(
                text=line,
                font_size=int(font_size.get()),
                text_color=text_color.get(),
                bg_color=bg_color.get(),
                position=position.get(),
                border_radius=int(border_radius.get()),
                text_pos=text_position.get()
            )
            img.save(f"{output_dir}/image_{idx+1}.png")

    messagebox.showinfo("Готово", "Субитры успешно созданы!")

# Обработчик для перемещения текста мышью
def start_drag(event):
    text_position.set((event.x * 4, event.y * 4))  # Масштабируем для полноразмерного изображения
    update_preview()

# Настройка GUI
root = tk.Tk()
root.title("Создание субтитров для шортсов")

# Настройки
text_color = tk.StringVar(value="#000000")
bg_color = tk.StringVar(value="#ffffff")
font_size = tk.StringVar(value="72")
position = tk.StringVar(value="center")
border_radius = tk.StringVar(value="20")
text_position = tk.Variable(value=None)
preview_text = tk.StringVar(value="Sample text")

# GUI элементы
tk.Label(root, text="Размер шрифта:").grid(row=0, column=0)
font_size_options = ["12", "24", "36", "48", "72", "96", "120"]
font_size.set(font_size_options[4])
tk.OptionMenu(root, font_size, *font_size_options, command=update_preview).grid(row=0, column=1)

tk.Label(root, text="Цвет текста:").grid(row=1, column=0)
tk.Button(root, text="Выбрать цвет", command=choose_text_color).grid(row=1, column=1)

tk.Label(root, text="Цвет фона бокса:").grid(row=2, column=0)
tk.Button(root, text="Выбрать цвет", command=choose_bg_color).grid(row=2, column=1)

tk.Label(root, text="Позиция текста:").grid(row=3, column=0)
tk.OptionMenu(root, position, "center", "top", "bottom", command=update_preview).grid(row=3, column=1)

tk.Label(root, text="Округление фона:").grid(row=4, column=0)
border_radius_options = ["0", "10", "20", "30"]
border_radius.set(border_radius_options[2])
tk.OptionMenu(root, border_radius, *border_radius_options, command=update_preview).grid(row=4, column=1)

tk.Label(root, text="Текст для предпросмотра:").grid(row=5, column=0)
tk.Entry(root, textvariable=preview_text, width=25).grid(row=5, column=1)
preview_text.trace("w", update_preview)

tk.Button(root, text="Создать субтитры", command=create_images).grid(row=6, columnspan=2)

# Добавляем область для предпросмотра
preview_label = tk.Label(root)
preview_label.grid(row=0, column=2, rowspan=7, padx=20, pady=10)
preview_label.bind("<B1-Motion>", start_drag)

# Инициализация предпросмотра
update_preview()

root.mainloop()
