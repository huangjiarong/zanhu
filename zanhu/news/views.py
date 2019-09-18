from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest, JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from zanhu.news.models import News
from zanhu.helpers import is_ajax, AuthorRequiredMixin


class NewsListView(LoginRequiredMixin, ListView):
    model = News
    paginate_by = 20
    template_name = 'news/news_list.html'

    def get_queryset(self):
        return News.objects.filter(reply=False)


class NewsDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    """删除动态"""
    template_name = 'news/news_confirm_delete.html'
    model = News
    success_url = reverse_lazy("news:list")


@login_required
@is_ajax
@require_http_methods(['POST'])
def post_news(request):
    """发送动态, Ajax Post请求"""
    post = request.POST['post'].strip()
    if post:
        posted = News.objects.create(user=request.user, content=post)
        return render(request, 'news/news_single.html', {'news': posted})
    else:
        return HttpResponseBadRequest("内容不能为空")


@login_required
@is_ajax
@require_http_methods(['POST'])
def like(request):
    """用户点赞, Ajax Post请求"""
    news_id = request.POST['news']
    news_obj = News.objects.get(uuid_id=news_id)
    #点赞或者取消赞
    news_obj.switch_liked(request.user)
    #返回赞的数量
    return JsonResponse({'likes': news_obj.count_likers()})


@login_required
@is_ajax
@require_http_methods(["GET"])
def get_thread(request):
    """返回动态的评论，AJAX GET请求"""
    news_id = request.GET['news']
    news = News.objects.get(pk=news_id)
    # render_to_string()表示加载模板，填充数据，返回字符串
    #要评论的原来那条数据
    news_html = render_to_string("news/news_single.html", {"news": news})
    #所有评论
    thread_html = render_to_string("news/news_thread.html", {"thread": news.get_thread()})  # 有评论的时候
    return JsonResponse({
        "uuid": news_id,
        "news": news_html,
        "thread": thread_html,
    })


@login_required
@is_ajax
@require_http_methods(["POST"])
def post_comment(request):
    """评论，AJAX POST请求"""
    post = request.POST['reply'].strip()
    parent_id = request.POST['parent']
    parent = News.objects.get(pk=parent_id)
    if post:
        parent.reply_this(request.user, post)
        return JsonResponse({'comments': parent.comment_count()})
    else:  # 评论为空返回400.html
        return HttpResponseBadRequest("内容不能为空！")

