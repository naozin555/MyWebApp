import matplotlib.pyplot as plt
import matplotlib
from django.shortcuts import redirect
import pandas as pd
from .models import Board, FoodHabitModel
import io
import os


class Service:

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
        # 食事の欠損値を最頻値で補完
        food_habit_df["食品名"].fillna(food_habit_df["食品名"].mode()[0], inplace=True)
        # 体重の欠損値を平均値で補完
        food_habit_df["体重"].fillna(food_habit_df["体重"].mean(), inplace=True)
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

    # バックエンドでの使用を指定
    matplotlib.use('Agg')

    @staticmethod
    def visualize_food_habit(post_pk):
        """グラフの描画"""
        # グラフを表示する領域の確保
        fig = plt.figure(facecolor='lightcyan', tight_layout=True)

        # グラフ位置の指定
        weight_graph = fig.add_subplot(1, 2, 1)
        food_category_graph = fig.add_subplot(1, 2, 2)

        # DBからデータの取得
        food_habit_data = FoodHabitModel.objects.filter(post_id=post_pk)
        date_list = [data.date for data in food_habit_data]
        weight_list = [data.weight for data in food_habit_data]
        food_category_list = [data.food_category for data in food_habit_data]

        # 体重推移の描画
        weight_graph.plot(date_list, weight_list)
        weight_graph.set_ylabel("Weight[kg]")
        weight_graph.set_xlabel("Date")
        weight_graph.set_ylim(50, 70)
        weight_graph.tick_params(axis='x', rotation=45)

        # 食事のカテゴリの割合の描画
        num_yellow = food_category_list.count('黄')
        num_red = food_category_list.count('赤')
        num_green = food_category_list.count('緑')
        food_category_num_list = [num_yellow, num_red, num_green]
        food_category_label = ["yellow", "red", "green"]
        colorlist = ["gold", "orangered", "lawngreen"]
        food_category_graph.pie(food_category_num_list, labels=food_category_label, autopct="%1.1f%%", colors=colorlist,
                                wedgeprops={'linewidth': 1, 'edgecolor': "black"})

        # 食事のバランスに対するアドバイス
        food_category_map = {'黄': num_yellow, '赤': num_red, '緑': num_green}
        min_category = min(food_category_map, key=food_category_map.get)
        min_category_num = min(food_category_map.values())
        max_category_num = max(food_category_map.values())
        if max_category_num > 1.5 * min_category_num:
            msg = f"バランスが偏っています。{min_category}色の食品をより多く摂取しましょう。"
        else:
            msg = "この調子で、バランスの良い食事を心がけましょう。"

        return msg


    @staticmethod
    def plt_to_svg():
        """svgへの変換"""
        # ファイルに書き出さずに仮想的にメモリ上に保存するようにする
        buf = io.BytesIO()
        # 保存する
        plt.savefig(buf, format='svg', bbox_inches='tight')
        # 保存したグラフデータを読み込む
        graph = buf.getvalue()
        # メモリを開放する
        buf.close()
        return graph

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
