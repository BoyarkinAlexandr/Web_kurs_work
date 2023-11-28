from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .utils import create_invoice_pdf
from orders.models import Order

def invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    pdf_content = create_invoice_pdf(order)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=invoice_{order.id}.pdf'
    response.write(pdf_content.getvalue())
    return response
