from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm



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
                user_t = user_type(request.user)
                print(user_t)
                if (user_t == 'author' or user_t == 'publisher'):
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

# user type function
def user_type(username):
    user = User.objects.get(username=username)
    if Author.objects.filter(user=user).exists():
        return('author')
    elif Publisher.objects.filter(user=user).exists():
        return('publisher')
    else:
        return('user')

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


def get_authors_attributes(user, author):
    context = {
        'username': user.username,
        'user_type': user_type(user),
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': author.email,
        'age': author.age
    }
    return context


@ login_required(login_url='login')
def profile(request):
    user = request.user
    user_t = user_type(user)
    print(user_t)
    if (user_t == 'author'):
        author = Author.objects.get(user=user)
        context = get_authors_attributes(user, author)
    # elif (user_t == 'publisher'):
    #     publisher = Publisher.objects.get(user=user)
    #     context = get_publishers_attributes(user, publisher)
    # else:
    #     context = get_users_attributes(user)
    else:
        context = {}
    return render(request, 'library/profile.html', context)


@ login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()

            user = authenticate(request, username=request.user.username,
                                password=form.cleaned_data.get('new_password2'))

            login(request, user)
            message = 'You have successfully changed your password'
            return redirect('success', message=message)
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'library/change_password.html', {'form': form})