from django.shortcuts import render
from django.http import Http404
from . models import category,products,User
from .forms import CustomUserChangeForm,ProductForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
from .forms import CommentForm
from .forms import RatingForm
from django.urls import reverse


def allProdCat(request,c_slug=None,id=None):
    c_page=None
    product=None
    if c_slug!=None:
        c_page=get_object_or_404(category,slug=c_slug)
        product=products.objects.all().filter(category_id=c_page)
    else:
        product=products.objects.all().filter()
    return render(request,"category.html",{'category':c_page,'products': product})

def proDetail(request, c_slug, product_slug):
    try:
        product = products.objects.get(category_id__slug=c_slug, slug=product_slug)
    except products.DoesNotExist:
        raise Http404("Product does not exist")
    return render(request, 'product.html', {'product': product})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)

            # Ensure the user instance exists
            user_instance = get_user_model().objects.filter(username=request.user.username).first()

            if user_instance:
                product.user = user_instance
                product.save()
                return redirect('/')  
            else:
                
                return render(request, 'user_not_found.html')

    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

@login_required
def edit_product(request, id):
    product = get_object_or_404(products, id=id)

    if request.user == product.user:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect(reverse('filmapp:prodCatdetail', args=[product.category_id.slug, product.slug]))
        else:
            form = ProductForm(instance=product)

        return render(request, 'edit_product.html', {'form': form, 'product': product})
    else:
        return redirect('/')
@login_required
def delete_product(request, id):
    product = get_object_or_404(products, id=id)

    if request.user == product.user:
        if request.method == 'POST':
            product.delete()
            return redirect('/')  
        else:
            return render(request, 'delete_product.html', {'product': product})
    else:
        return redirect('/')

@login_required
def add_comment(request, product_id):
    product = products.objects.get(id=product_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Ensure the user is authenticated
            if not request.user.is_authenticated:
                return redirect('login')  # Redirect to login if the user is not authenticated

            # Get the User instance explicitly
            user_instance = get_user_model().objects.get(pk=request.user.pk)

            comment = form.save(commit=False)
            comment.user = user_instance
            comment.product = product
            comment.save()
            return redirect(reverse('filmapp:prodCatdetail', args=[product.category_id.slug, product.slug]))
    else:
        form = CommentForm()

    return render(request, 'add_comment.html', {'form': form, 'product': product})


@login_required
def add_rating(request, product_id):
    product = products.objects.get(id=product_id)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            if not request.user.is_authenticated:
                return redirect('login')  

            user_instance = get_user_model().objects.get(pk=request.user.pk)

            rating = form.save(commit=False)
            rating.user = user_instance
            rating.product = product
            rating.save()
            return redirect(reverse('filmapp:prodCatdetail', args=[product.category_id.slug, product.slug]))
    else:
        form = RatingForm()
    return render(request, 'add_rating.html', {'form': form, 'product': product})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/edit_profile')  
    else:
        form = CustomUserChangeForm(instance=request.user)
        form.fields.pop('password')
        

    return render(request, 'edit_profile.html', {'form': form})