from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import activate
from docutils.languages import get_language

from .models import Category, Product
from cart.forms import CartAddProductForm

def product_list(request, category_slug=None):
    lang = request.GET.get('lang')
    if lang:
        current_lang = get_language()
        if current_lang != lang:
            activate(lang)
            request.session[get_language()] = lang
            return redirect(request.path)

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        language = get_language()  # используем get_language() вместо request.LANGUAGE_CODE
        category = get_object_or_404(Category,
                                     translations__language=language,
                                     translations__slug=category_slug)
        products = products.filter(category=category)

    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})



# def product_detail(request, id, slug):
#     product = get_object_or_404(Product,
#                                 id=id,
#                                 slug=slug,
#                                 available=True)
#     return render(request,
#                   'shop/product/detail.html',
#                   {'product': product})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, translations__slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product, 'cart_product_form': cart_product_form})

