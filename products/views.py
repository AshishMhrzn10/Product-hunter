from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils import timezone
# Create your views here.
def home(request):
    products = Product.objects.all().order_by('-votes_total')
    return render(request,'products/home.html',{'products':products})

@login_required(login_url='/accounts/signup')
def create(request):
    if request.method != "POST":
        return render(request,'products/create.html')
    else:
        title = request.POST['title']
        body = request.POST['body']
        url = request.POST['url']
        icon = request.FILES['icon']
        image = request.FILES['image']
        if title and body and url and icon and image:
            product = Product(title=title,body=body,icon=icon,image=image,hunter=request.user)
            product.pub_date = timezone.datetime.now()
            if url.startswith('http://') or url.startswith('https://'):
                product.url = url
            else:
                product.url = 'http://' + url
            product.save()
            return redirect('/products/'+str(product.id))
            
        else: 
            return render(request,'products/create.html',{'error':'All fields required'})
    return render(request,'products/create.html')


def detail(request,product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request,'products/detail.html',{'product':product})


@login_required(login_url='/accounts/signup')
def upvote(request,product_id):
    if request.method != "POST":
        return render(request,'products/home.html')
    else:
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('/products/'+str(product.id))