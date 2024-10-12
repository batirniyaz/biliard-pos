# import win32print
# import win32ui
# import win32con
# from PIL import Image, ImageWin


def format_order(order):
    def format_number(number):
        return f"{number:,}".replace(",", " ")
    products_count = {}
    options_count = {}
    for product in order['products']:
        product_name = product.get('product_name') or product.get('name')
        if product_name:
            products_count[product_name] = products_count.get(
                product_name, 0) + 1
        else:
            print(f"Предупреждение: продукт без имени: {product}")
    for option in order['options']:
        option_name = option.get('option_name') or option.get('name')
        if option_name:
            options_count[option_name] = options_count.get(
                option_name, 0) + 1
        else:
            print(f"Предупреждение: опция без имени: {option}")
    options_list = ", ".join(
        [f"{name} x{count}" for name, count in options_count.items()])
    products_list = ", ".join(
        [f"{name} x{count}" for name, count in products_count.items()])

    formatted_order = f"""
        Заказ завершен на столе '{order['table_name']}' с ID заказа: {order['id']}
        Общая цена: {format_number(order['total'])} UZS
        Время начала: {order['start_time']}
        Время окончания: {order['end_time']}
        Продолжительность: {order['duration']} минут
        Цена стола: {format_number(order['table_price'])} UZS
        Цена стола за {order['duration']} минут: {format_number(order['table_income'])} UZS
        Цена продуктов: {format_number(order['products_income'])}
        Цена опций: {format_number(order['options_income'])} UZS

        Продукты: {products_list}
        Опции: {options_list}
    """
    print("Отформатированный текст заказа:")
    print(formatted_order)
    return formatted_order


def prn_txt(order, printer_name="XP-58"):
    print("I am in prn_txt")
    return {"it works": order}

# def prn_txt(order, printer_name="XP-58"):
#     if printer_name is None:
#         printer_name = win32print.GetDefaultPrinter()
#
#     formatted_order = format_order(order)
#
#     try:
#         # Открыть изображение с помощью PIL
#         image_path = "logo.png"
#         img = Image.open(image_path)
#         resized_img = img.resize((300, 300))
#         hDC = win32ui.CreateDC()
#         hDC.CreatePrinterDC(printer_name)
#         print("Контекст устройства создан.")
#
#         # Получаем размеры страницы принтера
#         page_width = hDC.GetDeviceCaps(win32con.PHYSICALWIDTH)
#         # Получаем размеры измененного изображения
#         img_width, img_height = resized_img.size
#         # Вычисляем координату x для центрирования изображения
#         x = (page_width - img_width) // 2
#
#         hDC.StartDoc("Кириллический документ")
#         hDC.StartPage()
#
#         dib = ImageWin.Dib(resized_img)
#         dib.draw(hDC.GetHandleOutput(), (x, 0, x + img_width, img_height))
#         print("Изображение напечатано.")
#
#         font = win32ui.CreateFont({
#             "name": "Arial",
#             "height": 24,
#             "weight": win32con.FW_NORMAL,
#             "charset": win32con.RUSSIAN_CHARSET
#         })
#         hDC.SelectObject(font)
#         print("Шрифт создан и применён.")
#
#         x, y = 0, img_height  # Начинаем печать текста после изображения
#         line_height = 30
#         # Максимальная ширина строки в пикселях (с небольшим отступом)
#         max_width = page_width - 20
#
#         lines = formatted_order.strip().split('\n')
#         for line in lines:
#             words = line.split()
#             current_line = ""
#             for word in words:
#                 test_line = current_line + " " + word if current_line else word
#                 width = hDC.GetTextExtent(test_line)[0]
#                 if width <= max_width:
#                     current_line = test_line
#                 else:
#                     # Если текущее слово не помещается, печатаем текущую строку
#                     print(f"Печатаем строку на позиции y={y}: {current_line}")
#                     hDC.TextOut(x, y, current_line)
#                     y += line_height
#                     current_line = word  # Начинаем новую строку с текущего слова
#
#             # Печатаем оставшуюся часть строки
#             if current_line:
#                 print(f"Печатаем строку на позиции y={y}: {current_line}")
#                 hDC.TextOut(x, y, current_line)
#                 y += line_height
#
#             # Добавляем дополнительный отступ между абзацами
#             y += line_height // 2
#
#         try:
#             hDC.EndPage()
#         except win32ui.error as e:
#             if e.args[0] == -1:
#                 print(
#                     "Предупреждение: EndPage вернул -1. Это может быть нормально для некоторых принтеров.")
#             else:
#                 print(f"Ошибка при завершении страницы: {e}")
#                 return False
#
#         try:
#             hDC.EndDoc()
#         except Exception as e:
#             print(f"Ошибка при завершении документа: {e}")
#             return False
#
#         hDC.DeleteDC()
#         print("Печать завершена успешно.")
#         return True
#     except Exception as e:
#         print(f"Ошибка при печати: {e}")
#         return False