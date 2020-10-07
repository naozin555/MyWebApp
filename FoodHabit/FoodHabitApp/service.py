from django.shortcuts import redirect
import os
import pandas as pd
from .models import Board, FoodHabitModel


class Service:

    # アップロードされたファイルのハンドル
    def handle_uploaded_file(self, uploaded_file, upload_dir, post_pk):
        csv_filepath = os.path.join(upload_dir, uploaded_file.name)
        with open(csv_filepath, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        self._register_data(csv_filepath, post_pk)
        # アップロードしたファイルを削除
        os.remove(csv_filepath)

    @staticmethod
    def _register_data(csv_filepath, post_pk):
        """csvのデータをDBに登録する"""
        food_habit_df = pd.read_csv(csv_filepath)
        # 欠損値のあるレコードを除去
        food_habit_df.dropna(how='any', inplace=True)
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
        post = Board.objects.get(pk=pk)
        post.good += 1
        post.save()

    @staticmethod
    def press_read(request, pk):
        post = Board.objects.get(pk=pk)
        reader = request.user.get_username()
        if reader in post.previous_readers:
            return redirect('list')
        else:
            post.read += 1
            post.previous_readers = post.previous_readers + '' + reader
            post.save()
            return redirect('list')
