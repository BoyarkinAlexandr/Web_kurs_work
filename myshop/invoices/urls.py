from django.urls import path
from .views import invoice_pdf

urlpatterns = [
    path('<int:order_id>/invoice/', invoice_pdf, name='invoice_pdf'),
]
