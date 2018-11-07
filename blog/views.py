from django.shortcuts import render, get_object_or_404, reverse
from .models import Post, Category
from comments.forms import CommentForm
import markdown
from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


def index(request):
    posts = Post.objects.all().order_by('-created_time')
    paginator = Paginator(posts, 4)
    post_list = paginator.page(1)
    return render(request, 'blog/index.html', {'post_list': post_list})


# 分页显示
def get_page(request, page):
    posts = Post.objects.all().order_by('-created_time')
    paginator = Paginator(posts, 4)
    try:
        post_list = paginator.page(int(page))
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'blog/index.html', {'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    # 记得在顶部导入 CommentForm
    form = CommentForm()

    # 获取这篇post下的全部评论
    comment_list = post.comment_set.all()

    context = {'post': post,
               'form': form,
               'comment_list': comment_list}

    return render(request, 'blog/detail.html', context=context)


# 归档视图
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', {'post_list': post_list})


# 分类视图
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', {'post_list': post_list})


# 标签视图
def tag(request, pk):
    post_list = Post.objects.filter(tags=pk).order_by('-created_time')
    return render(request, 'blog/index.html', {'post_list': post_list})


class RSSFeed(Feed):
    title = "RSS feed - blog"
    link = "rss/"
    description = "RSS feed - blog posts"

    def items(self):
        return Post.objects.all().order_by("-created_time")

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return item.get_absolute_url()
