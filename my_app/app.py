# ==================================================
# app.py
# 以下の初期化を行う
# ・ユーザ管理を行うflask_login
# ・DB構成管理を行うflask_migrate
# ・flaskのモジュール分割を可能にするblueprint
# ==================================================
from flask import Flask
from flask_migrate import Migrate
from .models import db, User
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
# Blueprintのモジュールをインポート
from .auth.views import auth_bp
from .memo.views import memo_bp
from .wiki.views import wiki_bp

# Flaskクラスのインスタンスを作成
app = Flask(__name__)
# 設定ファイル読み込み、config.pyモジュールのConfigクラスを読み込む
# Note: 実行ディレクトリからのパスを記述する必要があることに注意
app.config.from_object("my_app.config.ProductionConfig")
# dbとFlaskとの紐づけ
db.init_app(app)
# マイグレーションとの紐づけ（Flaskとdb）
migrate = Migrate(app, db)
# LoginManagerインスタンス
login_manager = LoginManager()
# LoginManagerとFlaskとの紐づけ
login_manager.init_app(app)
# ログインが必要なページにアクセスしようとしたときに表示されるメッセージを変更
login_manager.login_message = "認証していません：ログインしてください"
# 未認証のユーザーがアクセスしようとした際にリダイレクトされる関数名を設定する(ブループリント対応)
login_manager.login_view = 'auth.login'

# アプリケーションルートを取得
app_root = app.config.get("APPLICATION_ROOT", "/")

# blueprintをアプリケーションに登録
app.register_blueprint(auth_bp, prefix=f'{app_root}/auth')
app.register_blueprint(memo_bp, prefix=f'{app_root}/memo')
app.register_blueprint(wiki_bp, prefix=f'{app_root}/wiki')

# ProxyFixの設定
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# デバグ用あ
from flask import request
@app.before_request
def log_request_info():
    print('Path:', request.path)
    print('Host:', request.host)
    print('Remote Addr:', request.remote_addr)
    print('Schema:', request.scheme)

# viewsのインポート
from .views import *

# ==================================================
# 実行
# ==================================================
if __name__ == "__main__":
    app.run()