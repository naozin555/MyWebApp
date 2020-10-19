import matplotlib
import matplotlib.pyplot as plt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import UploadFileForm
from .models import Board, FoodHabitModel
from .service import Service

service = Service()


# ユーザー登録
def sign_up_func(request):
    if request.method == 'POST':
        new_username = request.POST['username']
        new_password = request.POST['password']

        # noinspection PyBroadException
        try:
            User.objects.get(username=new_username)
            return render(request, 'signup.html', {'error': 'このユーザーは既に登録されています。'})
        except Exception:
            user = User.objects.create_user(new_username, '', new_password)
            return redirect('login')
    return render(request, 'signup.html')


# ログイン
def log_in_func(request):
    if request.method == 'POST':
        enterd_username = request.POST['username']
        enterd_password = request.POST['password']
        user = authenticate(request, username=enterd_username, password=enterd_password)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return render(request, 'login.html', {'error': 'ユーザー名かパスワードが違います。'})
    return render(request, 'login.html')


# ログアウト
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
            service.register_uploaded_csvfile_data(request.FILES['file'], post.pk)
            return redirect('list')
    else:
        form = UploadFileForm()
        return render(request, 'create.html', {'form': form})
    return render(request, 'create.html', {'form': form})


# 記事一覧
@login_required()
def list_func(request):
    object_list = Board.objects.all()
    return render(request, 'list.html', {'object_list': object_list})


# 記事の詳細
def detail_func(request, pk):
    # バックエンドでの使用を指定(これを記載しないと「pythonが予期しない理由で終了しました。」というエラーが発生する)
    matplotlib.use('Agg')
    # 食習慣に対するアドバイス生成
    advice_msg = service.make_advice_msg(pk)
    post_detail = Board.objects.get(pk=pk)
    return render(request, 'detail.html', {'post_detail': post_detail, 'advice_msg': advice_msg})


# 記事の詳細に画像を埋め込むためのview
def plot_func(request, pk):
    # バックエンドでの使用を指定(これを記載しないと「pythonが予期しない理由で終了しました。」というエラーが発生する)
    matplotlib.use('Agg')
    # 食習慣の可視化（戻り値はアドバイス）
    service.visualize_food_habit(pk)
    # svgで保存
    svg = service.plt_to_svg()
    # グラフのクリーンアップ
    plt.cla()
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response


# いいね
def good_func(request, pk):
    service.press_good(pk)
    return redirect('list')


# 既読
def read_func(request, pk):
    return service.press_read(request, pk)


# 投稿削除
def delete_func(request, pk):
    # 記事の削除
    post = Board.objects.get(pk=pk)
    post.delete()
    # 削除する記事に紐づく食習慣データの削除
    FoodHabitModel.objects.filter(post_id=pk).delete()
    return redirect('list')
