from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

@login_required(login_url='login')
def home(request):
    # Logic
    books = Book.objects.all()
    # Context
    context = {
        'books':books

    }
    return render(request, 'index.html', context)

# Success and fail views


def success(request, message=None):
    return render(request, 'library/success.html', {'message': message})


def fail(request, message=None):
    return render(request, 'library/fail.html', {'message': message})



# example view
def example(request):
    # Logic
    # Context
    publisher_form = PublisherForm()
    author_form = AuthorForm()
    lib_user_form = LibraryUserForm()
    context = {
        'publisher_form':publisher_form,
        'author_form':author_form,
        'lib_user_form':lib_user_form,

    }
    return render(request, 'example.html', context)


# Author Regisration 
def author_registration(request):
    if request.method =='POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()

            # Get data to craete author in DB
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            age = form.cleaned_data.get('age')
            user = User.objects.get(username=username)
            author = Author(user=user, email=email, age=age)
            author.save()

            # Authenticate User
            user = authenticate(request, username=username, password=password)
            login(request,user)
            return redirect('home')
    
    else:
        form = AuthorForm()
        
    

    # print(username)
    context = {
       'form':form, 
    }
    return render(request, 'library/author_registration.html', context)

def loginview(request):
    form = LoginForm()
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                
                return redirect('home')
            else:
                return redirect('login')
        else:
             form = LoginForm()
    context = {
        'form':form
    }
    return render(request, 'library/login.html', context)

@login_required(login_url='login')
def add_book(request):
    form = BookForm()
    if request.method =='POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            message = 'Book was added'
            return redirect('success', message='Book was added' )
    else:
        form = BookForm()
    context = {
        'form':form
    }
    return render(request, 'library/add-book.html', context)

def signout(request):
    logout(request)
    # return redirect('/')
    context = {}
    return render(request, 'library/logout.html', context)


@login_required(login_url='login')
def mybooks(request):
    # Logic
    books = Book.objects.all()
    # Context
    context = {
        'books':books

    }
    return render(request, 'library/mybooks.html', context)


@login_required(login_url='login')
def edit_book(request,pk):
        book = Book.objects.get(id=pk)
        form = BookForm(instance=book)
        if request.method == 'POST':
            form = BookForm(request.POST, instance=book)
            if form.is_valid():
                form.save()
                return redirect('mybooks')

        context = {
            'form': form,
        }
        return render(request, 'library/edit_book.html', context)


@login_required(login_url='login')
def delete_book(request, pk):
    book = Book.objects.get(id=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('success', message='Item was deleted')
    context = {
        'book': book,
    }
    return render(request, 'library/delete-book.html', context)
