from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import DeleteView
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
            return render(request, 'signup.html', {'some': 100})
    return render(request, 'signup.html', {'some': 100})


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
    return render(request, 'login.html', {'some': 100})


def log_out_func(request):
    logout(request)
    return redirect('login')


# アップロードされたファイルのハンドル
def _handle_uploaded_file(f):
    csv_filepath = os.path.join(UPLOAD_DIR, f.name)
    with open(csv_filepath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    # csvデータをDBに登録する
    print("csvを開けます")
    print(csv_filepath)
    food_habit_df = pd.read_csv(csv_filepath)
    print(food_habit_df)
    for i in (food_habit_df['日付']):
        print(i)
    food_habit_instances = [FoodHabitModel.objects.bulk_create(
        date=date,
        weight=weight,
        food_name=food_name,
        food_category=food_category,
    ) for date, weight, food_name, food_category in zip(food_habit_df['日付'], food_habit_df['体重'],
                                                        food_habit_df['食品名'], food_habit_df['食品のカテゴリ'])]
    print(food_habit_instances)
    FoodHabitModel.objects.bulk_create(food_habit_instances)
    os.remove(csv_filepath)  # アップロードしたファイルを削除


# 新規投稿（ファイルのアップロード）
def create_post_func(request):
    if request.method == 'POST':
        Board.objects.create(author=request.user.get_username())
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            _handle_uploaded_file(request.FILES['file'])
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
    post2 = request.user.get_username()
    if post2 in post.readtext:
        return redirect('list')
    else:
        post.read += 1
        post.readtext = post.readtext + '' + post2
        post.save()
        return redirect('list')


class FoodHabitDelete(DeleteView):
    template_name = 'delete.html'
    model = Board
    success_url = reverse_lazy('list')


def hello_func(request):
    return HttpResponse("<h1>ようこそ</h1>")
