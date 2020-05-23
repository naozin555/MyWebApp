from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import BoardModel
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


# Create your views here.
def signup_func(request):
    if request.method == 'POST':
        username2 = request.POST['username']
        password2 = request.POST['password']
        try:
            User.objects.get(username=username2)
            return render(request, 'signup.html', {'duplicated_user_error': 'このユーザーは登録されています。'})
        except:
            user = User.objects.create_user(username2, '', password2)
            return render(request, 'signup.html')
    return render(request, 'signup.html')


def login_func(request):
    if request.method == 'POST':
        username2 = request.POST['username']
        password2 = request.POST['password']
        user = authenticate(request, username=username2, password=password2)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return redirect('login')
    return render(request, 'login.html')


@login_required
def list_func(request):
    object_list = BoardModel.objects.all()
    return render(request, 'list.html', {'object_list': object_list})


def logout_func(request):
    logout(request)
    return redirect('login')


def detail_func(request, pk):
    object = BoardModel.objects.get(pk=pk)
    return render(request, 'detail.html', {'object': object})


def good_func(request, pk):
    post = BoardModel.objects.get(pk=pk)
    post.good += 1
    post.save()
    return redirect('list')


def read_func(request, pk):
    post = BoardModel.objects.get(pk=pk)
    reader = request.user.get_username()
    if reader in post.read_user:
        return redirect('list')
    else:
        post.read += 1
        post.read_user = post.read_user + '' + reader
        post.save()
        return redirect('list')


class Create(CreateView):
    template_name = 'create.html'
    model = BoardModel
    fields = ('title', 'content', 'author', 'images')
    success_url = reverse_lazy('list')

