# ==================================================
# config.py
# Flaskの動作設定のクラスを作成する
# app.pyで読み込むクラスを指定する
# 開発用や本番用といったサブクラスを作ることで、環境ごとの設定の差分だけを管理可能
# ==================================================
class Config(object):
    # 環境共通の設定
    # デバッグモード
    DEBUG=False
    # CSRFやセッションで使用
    # ToDo: 環境変数から設定できるように変更する
    SECRET_KEY = "secret-key"
    # 警告対策
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # データベース接続の安定化オプション
    # Azure SQL DatabaseなどのクラウドDBでは必須級の設定
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,  # 接続を利用する直前に「SELECT 1」などで生存確認を行う（切断されていたら再接続する）
        "pool_recycle": 1800,   # 1800秒（30分）経過した接続を破棄し、新しい接続を作り直す（Azureのロードバランサによる切断対策）
        "pool_timeout": 30,     # 接続プールが空の場合の待機時間（秒）
        "pool_size": 10,        # プール内に維持する接続数（必要に応じて調整）
        "max_overflow": 10,     # プールサイズを超えて作成できる一時的な接続数
    }

class DevelopmentConfig(Config):
    # 開発環境用の設定
    DEBUG = True
    # ローカル開発環境用のSQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.sqlite'

import os
import urllib
class ProductionConfig(Config):
    # 本番環境用の設定
    # 環境変数から取得（パスワードなどは直書きしないこと）
    db_user     = os.environ.get("DB_USER", "")
    db_password = urllib.parse.quote_plus(os.environ.get("DB_PASSWORD", "")) # パスワードに含まれる特殊文字をエンコード
    db_server   = os.environ.get("DB_SERVER", "")
    db_name     = os.environ.get("DB_NAME", "")
    # 接続URIの組み立て
    SQLALCHEMY_DATABASE_URI = f"mssql+pymssql://{db_user}:{db_password}@{db_server}:1433/{db_name}"