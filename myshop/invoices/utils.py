from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import locale
from django.utils.translation import get_language


def create_invoice_pdf(order):
    language = get_language()
    buffer = BytesIO()

    # Регистрируем шрифт из локального файла
    pdfmetrics.registerFont(TTFont('Ubuntu', 'static/fonts/Roboto-Black.ttf'))

    # Создаем PDF-документ с указанным шрифтом
    p = canvas.Canvas(buffer)
    p.setFont('Ubuntu', 12)  # Замените 12 на нужный вам размер шрифта

    # Определение заголовков в зависимости от языка сайта
    if language == 'ru':
        text_dict = {
            'invoice': 'Счет на оплату по заказу',
            'separator': '----------------------------------------',
            'header': 'Товар             Количество        Цена',
            'total': 'Итого',
        }
    elif language == 'en':
        text_dict = {
            'invoice': 'Invoice for order',
            'separator': '----------------------------------------',
            'header': 'Product          Quantity         Price',
            'total': 'Total',
        }
    else:
        # Если выбран неизвестный язык, используем английские заголовки по умолчанию
        text_dict = {
            'invoice': 'Invoice for order',
            'separator': '----------------------------------------',
            'header': 'Product          Quantity         Price',
            'total': 'Total',
        }

    # Добавляем текст и форматирование
    p.drawString(100, 800, f'{text_dict["invoice"]} #{order.id}')
    p.drawString(100, 780, text_dict["separator"])
    p.drawString(100, 760, text_dict["header"])

    y = 740
    for item in order.items.all():
        product_name = item.product.name[:20] if len(item.product.name) > 20 else item.product.name
        p.drawString(100, y, f'{product_name:20} {item.quantity:10} {item.get_total_price():.2f}')
        y -= 20

    p.drawString(100, y, text_dict["separator"])
    p.drawString(100, y - 20, f'{text_dict["total"]}: {order.get_total_cost():.4f}')

    # Закрываем PDF
    p.showPage()
    p.save()

    # Сбрасываем буфер
    buffer.seek(0)

    return buffer