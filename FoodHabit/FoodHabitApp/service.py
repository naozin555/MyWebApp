import matplotlib.pyplot as plt
from django.shortcuts import redirect
import os
import pandas as pd
from .models import Board, FoodHabitModel
import io


class Service:

    @staticmethod
    def graph_plot(post_pk):
        """グラフの描画"""
        food_habit_data = FoodHabitModel.objects.filter(post_id=post_pk)
        # 日付け
        x = [data.date for data in food_habit_data]
        y = [data.weight for data in food_habit_data]
        plt.plot(x, y)

    @staticmethod
    def plt_to_svg():
        """svgへの変換"""
        buf = io.BytesIO()
        plt.savefig(buf, format='svg', bbox_inches='tight')
        s = buf.getvalue()
        buf.close()
        return s

    def handle_uploaded_file(self, uploaded_file, upload_dir, post_pk):
        """アップロードされたファイルのハンドル"""
        csv_filepath = os.path.join(upload_dir, uploaded_file.name)
        with open(csv_filepath, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        self._register_data(csv_filepath, post_pk)
        # アップロードしたファイルを削除
        os.remove(csv_filepath)

    def _register_data(self, csv_filepath, post_pk):
        """csvのデータをDBに登録する"""
        food_habit_df = pd.read_csv(csv_filepath)
        # 欠損値のあるレコードを除去
        food_habit_df.dropna(how='any', inplace=True)
        # 食品名から食品のカテゴリを割り当てる
        food_habit_df['食品のカテゴリ'] = food_habit_df.apply(self._assign_food_category, axis=1)
        # DB登録
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

    @staticmethod
    def press_good(pk):
        """いいねボタンが押された数を計算する"""
        post = Board.objects.get(pk=pk)
        post.good += 1
        post.save()

    @staticmethod
    def press_read(request, pk):
        """既読ボタンが押された数を計算する"""
        post = Board.objects.get(pk=pk)
        reader = request.user.get_username()
        if reader in post.previous_readers:
            return redirect('list')
        else:
            post.read += 1
            post.previous_readers = post.previous_readers + '' + reader
            post.save()
            return redirect('list')

    @staticmethod
    def _assign_food_category(row):
        """食品名に応じて、カテゴリを割り当てる"""
        if "焼肉" in row["食品名"] or "ハンバーグ" in row["食品名"] or "焼き魚" in row["食品名"]:
            return "赤"
        elif "ピーマン炒め" in row["食品名"] or "ほうれん草のおひたし" in row["食品名"] or "切り干し大根" in row["食品名"]:
            return "緑"
        elif "うどん" in row["食品名"] or "チャーハン" in row["食品名"] \
                or "フライドポテト" in row["食品名"] or "カップヌードル" in row["食品名"]:
            return "黄"
        else:
            print(f"想定外の食品名です：{row['食品名']}")
