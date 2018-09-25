# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import markdown

from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse

# Create your views here.
from comments.forms import CommentForm
from .models import Post, Category


# 主页
def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 详情
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 阅读量加1
    post.increase_views()

    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()

    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }
    return render(request, 'blog/detail.html', context=context)


# 归档
def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    )
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 分类
def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})
