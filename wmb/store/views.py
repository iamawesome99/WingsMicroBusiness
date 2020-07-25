from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datastructures import MultiValueDictKeyError

from . import forms
from .models import Product, Branch, SpecificProduct, ProductImage

MAIN_BRANCH_NAME = "microbuisness"


def add_to_cart(request, item):
    try:
        request.session['cart'].append(item)
    except KeyError or AttributeError:
        request.session['cart'] = [item]
    finally:
        request.session.modified = True


def make_cart(request):
    request.session['cart'] = []
    request.session.modified = True


def remove_from_cart(request, location):
    try:
        request.session['cart'].pop(location)
    except KeyError or AttributeError:
        pass
    finally:
        request.session.modified = True


def cart_size(request):
    try:
        return len(request.session['cart'])
    except KeyError:
        return 0


def base_context(request):
    return {"cart_size": cart_size(request)}


def index(request):
    branches = Branch.objects.exclude(name=MAIN_BRANCH_NAME)

    context = base_context(request)
    context.update({'branch': get_object_or_404(Branch, name=MAIN_BRANCH_NAME),
                    'branches': branches})
    return render(request, 'store/index.html', context)


def branch_detail(request, branch):
    if branch == MAIN_BRANCH_NAME:
        return redirect('index')

    branch_object = get_object_or_404(Branch, name=branch)

    context = base_context(request)
    context.update({'branch': branch_object,
                    'title': branch_object.display_name})
    return render(request, 'store/branch_details.html', context)


def branch_products(request, branch):
    branch_object = get_object_or_404(Branch, name=branch)

    context = base_context(request)
    context.update({'branch': branch_object,
                    'title': branch_object.display_name,
                    'products': Product.objects.filter(branch=branch_object) |
                                Product.objects.filter(other_branches=branch_object)})

    return render(request, 'store/product_list.html', context)


def product_detail(request, branch, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if branch != product.branch.name:
        return redirect('product_detail', branch=product.branch.name, product_id=product_id)

    ops_price = []

    for i in product.options.options:
        ops_price.extend([("id_" + i.name + "_" + str(c), p) for c, p in zip(range(len(i.del_price)), i.del_price)])

    pictures = ProductImage.objects.filter(product=product)

    context = base_context(request)
    context.update({'product': product,
                    'branch': product.branch,
                    'title': product.name + " - " + product.branch.display_name,
                    'ops_price': ops_price,
                    'pictures': pictures
                    })

    if ops_price:
        context['form'] = forms.OptionsForm(product.options,
                                            initial={i.name: i.choices[0] for i in product.options.options})

    print(context)

    return render(request, 'store/product_details.html', context)


def buy(request, branch, product_id):
    print(request.POST)

    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)

        add_to_cart(request, SpecificProduct(product, request.POST.dict()).encode())

        context = base_context(request)
        context.update({'branch': product.branch,
                        'cart_items': [str(h) for h in request.session['cart']]
                        })

        messages.success(request, 'Added ' + product.name + " to your cart")

    return redirect('cart', branch=branch)


def cart(request, branch):
    try:
        request.session['cart']
    except KeyError:
        make_cart(request)

    cart_items = [SpecificProduct.decode(x) for x in request.session['cart']]
    total = sum([x.price for x in cart_items])
    context = base_context(request)
    context.update({'branch': get_object_or_404(Branch, name=branch),
                    'cart_items': cart_items,
                    'total': total
                    })
    return render(request, 'store/cart.html', context=context)


def remove_cart(request, branch, number):
    try:
        product = get_object_or_404(Product, pk=int(request.session['cart'][number].split("|")[0]))
        remove_from_cart(request, number)
        messages.success(request, 'Removed ' + product.name + " from your cart")
    except IndexError:
        messages.error(request, "Couldn't find that item in your shopping cart")
    finally:
        return redirect(cart, branch=branch)


def clear_cart(request, branch):
    request.session['cart'] = []
    request.session.modified = True
    return redirect(cart, branch=branch)


def search(request, branch):
    branch_object = get_object_or_404(Branch, name=branch)

    try:
        request.GET['query']
    except MultiValueDictKeyError:
        return render(request, 'store/search.html', {'branch': branch_object, 'title': branch_object.display_name,
                                                     'no_query': True})

    context = base_context(request)

    if branch != "microbuisness":
        products = Product.objects.filter(branch=branch_object, name__contains=request.GET['query']) | \
                   Product.objects.filter(other_branches=branch_object, name__contains=request.GET['query'])
    else:
        products = Product.objects.filter(name__contains=request.GET['query'])

    context.update({'branch': branch_object, 'title': branch_object.display_name, 'post_data': request.GET['query'],
                    'products': products})

    if context['products']:
        return render(request, 'store/search.html', context)

    return render(request, 'store/search.html', context)