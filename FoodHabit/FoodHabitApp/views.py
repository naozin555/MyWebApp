from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .models import FoodHabitModel, Board
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UploadFileForm
import os
from django.contrib.auth.decorators import login_required
import pandas as pd


# アップロードしたファイルを保存するディレクトリ
UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + "/static/uploaded/"


# Create your views here.
def sign_up_func(request):
    if request.method == 'POST':
        new_username = request.POST['username']
        new_password = request.POST['password']
        try:
            User.objects.get(username=new_username)
            return render(request, 'signup.html', {'error': 'このユーザーは既に登録されています。'})
        except:
            user = User.objects.create_user(new_username, '', new_password)
            return render(request, 'signup.html')
    return render(request, 'signup.html')


def log_in_func(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return render(request, 'login.html', {'error': 'ログインする権限がありません。登録されいないユーザーである、もしくはユーザー名かパスワードが間違っています。'})
    return render(request, 'login.html')


def log_out_func(request):
    logout(request)
    return redirect('login')


# 新規投稿（ファイルのアップロード）
def create_post_func(request):
    if request.method == 'POST':
        post = Board.objects.create(author=request.user.get_username())
        post.save()
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            _handle_uploaded_file(request.FILES['file'], post.pk)
            return redirect('list')
    else:
        form = UploadFileForm()
        return render(request, 'create.html', {'form': form})
    return render(request, 'create.html', {'form': form})


@login_required()
def list_func(request):
    object_list = Board.objects.all()
    return render(request, 'list.html', {'object_list': object_list})


def detail_func(request, pk):
    object = Board.objects.get(pk=pk)
    return render(request, 'detail.html', {'object': object})


def good_func(request, pk):
    post = Board.objects.get(pk=pk)
    post.good += 1
    post.save()
    return redirect('list')


def read_func(request, pk):
    post = Board.objects.get(pk=pk)
    reader = request.user.get_username()
    if reader in post.previous_readers:
        return redirect('list')
    else:
        post.read += 1
        post.readtext = post.previous_readers + '' + reader
        post.save()
        return redirect('list')


class FoodHabitDelete(DeleteView):
    template_name = 'delete.html'
    model = Board
    success_url = reverse_lazy('list')


def hello_func(request):
    return HttpResponse("<h1>ようこそ</h1>")


# アップロードされたファイルのハンドル
def _handle_uploaded_file(f, post_pk):
    csv_filepath = os.path.join(UPLOAD_DIR, f.name)
    with open(csv_filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    # csvデータをDBに登録する
    food_habit_df = pd.read_csv(csv_filepath)
    post_pk_list = [post_pk] * len(food_habit_df)
    food_habit_instances = [FoodHabitModel(
        date=date,
        weight=weight,
        food_name=food_name,
        food_category=food_category,
        post_id=post_id
    ) for date, weight, food_name, food_category, post_id
        in zip(food_habit_df['日付'], food_habit_df['体重'],
               food_habit_df['食品名'], food_habit_df['食品のカテゴリ'], post_pk_list)]
    FoodHabitModel.objects.bulk_create(food_habit_instances)
    os.remove(csv_filepath)  # アップロードしたファイルを削除
