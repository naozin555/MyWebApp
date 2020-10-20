# 食習慣の可視化ツール

本ツールは1ヶ月の体重と食事のリストから、体重推移と食事のバランスをグラフで表示するツールです。

# イメージ

![スクリーンショット 2020-10-20 11 18 09](https://user-images.githubusercontent.com/37050583/96532027-f567a600-12c5-11eb-8ff7-a4d9cb237bdf.png)

# 特徴

食事のバランスを解析して、アドバイスをしてくれます。

# 使い方

1.[こちら](https://food-habit-analyzer.herokuapp.com/signup/)のサイトにアクセスする。  
2.ユーザー登録、ログインを済ませる。  
3.新規投稿ページへいき、サンプルファイルをダウンロードする  
4.サンプルファイルに体重と食事を記入する。  
5.新規投稿ページへファイルをアップロードする。  
6.詳細画面にいくと、グラフが表示される。

# 作者

* 作成者：原田直明
* E-mail：naozin555@gmail.com

## ローカルで動かす場合に必要なパッケージ等
### Requirement

asgiref==3.2.10  
certifi==2020.6.20  
cycler==0.10.0  
dj-database-url==0.5.0  
Django==3.1  
django-heroku==0.3.1  
gunicorn==20.0.4  
isort==5.6.3  
kiwisolver==1.2.0  
matplotlib==3.3.2  
numpy==1.19.2  
opencv-python==4.4.0.44  
pandas==1.1.3  
Pillow==7.2.0  
psycopg2-binary==2.8.6  
pyparsing==2.4.7  
python-dateutil==2.8.1  
pytz==2020.1  
six==1.15.0  
sqlparse==0.3.1  
whitenoise==5.2.0  

### Installation

pip install -r requirements.txt

