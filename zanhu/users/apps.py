from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "zanhu.users"
    verbose_name = '用户'
    verbose_name_plural = verbose_name

    def ready(self):
        try:
            import zanhu.users.signals  # noqa F401
        except ImportError:
            pass
