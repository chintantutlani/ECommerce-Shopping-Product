from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from .models import Product, Category
from .forms import ProductForm


@csrf_exempt
def ShowAllProducts(request):
    category = request.GET.get('category')

    if category == None:
        products = Product.objects.order_by('-id').filter(is_published=True)
        page_num = request.GET.get("page")
        paginator = Paginator(products, 2)
        try:
            products = paginator.page(page_num)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
    else:
        products = Product.objects.filter(category__name=category)

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories
    }

    return render(request, "template/showProduct.html", context)


@csrf_exempt
def productDetail(request, pk):
    eachProduct = Product.objects.get(id=pk)

    context = {
        'eachProduct': eachProduct,

    }

    return render(request, 'productDetail.html', context)


@csrf_exempt
def addProduct(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('showProducts')
    else:
        form = ProductForm()

    context = {
        "form": form
    }

    return render(request, 'addProduct.html', context)


@csrf_exempt
def updateProduct(request, pk):
    product = Product.objects.get(id=pk)

    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('showProducts')

    context = {
        "form": form
    }

    return render(request, 'updateProduct.html', context)


@csrf_exempt
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('showProducts')
