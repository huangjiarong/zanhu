from functools import wraps

from django.http import HttpResponseBadRequest
from django.views import View
from django.core.exceptions import PermissionDenied


def is_ajax(func):
    """判断一个请求是否是Ajax请求"""

    @wraps(func)
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest('不是Ajax请求')
        return func(request, *args, **kwargs)

    return wrap


class AuthorRequiredMixin(View):
   """
   验证是否为原作者, 用于状态删除和文章编辑
   """
   def dispatch(self, request, *args, **kwargs):
       #状态和文章都有user属性
       if self.get_object().user.username != self.request.user.username:
           raise PermissionDenied

       return super(AuthorRequiredMixin, self).dispatch(request, *args, **kwargs)
