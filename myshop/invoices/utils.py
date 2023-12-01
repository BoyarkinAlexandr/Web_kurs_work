from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.utils.translation import get_language

def create_invoice_pdf(order):
    language = get_language()
    buffer = BytesIO()

    # Register the font from a local file
    pdfmetrics.registerFont(TTFont('Ubuntu', 'static/fonts/Roboto-Black.ttf'))

    # Create a PDF document with the specified font
    p = canvas.Canvas(buffer)
    p.setFont('Ubuntu', 12)

    # Define headers based on the site language
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
        # Use English headers by default if an unknown language is selected
        text_dict = {
            'invoice': 'Invoice for order',
            'separator': '----------------------------------------',
            'header': 'Product          Quantity         Price',
            'total': 'Total',
        }

    # Add text and formatting
    p.drawString(100, 800, f'{text_dict["invoice"]} #{order.id}')
    p.drawString(100, 780, text_dict["separator"])
    p.drawString(100, 760, text_dict["header"])

    y = 740
    for item in order.items.all():
        product_name = item.product.name[:20] if len(item.product.name) > 20 else item.product.name
        # Adjust the X-coordinate for the Quantity column
        p.drawString(100, y, f'{product_name:20} {item.quantity:^10}   {item.get_total_price():.2f}')
        y -= 20

    p.drawString(100, y, text_dict["separator"])
    p.drawString(100, y - 20, f'{text_dict["total"]}: {order.get_total_cost():.4f}')

    # Close the PDF
    p.showPage()
    p.save()

    # Reset the buffer
    buffer.seek(0)

    return buffer
