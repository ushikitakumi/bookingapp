from .settings_common import *

DEBUG = False

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]

STATIC_ROOT = '/usr/share/nginx/html/static'


# ロギング設定
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # ロガーの設定
    'loggers': {
        # Djangoが利用するロガー
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        # bookingアプリケーションが利用するロガー
        'booking': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },

    # ハンドラーの設定
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR,'logs/django.logs'), 
            'formatter': 'prod',
            'when': 'D', # ログローテーション(毎日)
            'interval': 1, # ログローテーション間隔
            'backupCount': 7, # 保存しておくファイル数
        },
    },

    # フォーマッタの設定
    'formatters': {
        'prod': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(line:%(lineno)d)',
                '%(message)s',
            ])
        },
    },
}