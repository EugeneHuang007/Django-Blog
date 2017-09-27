import logging

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from django.db.models import Count

from blog.forms import CommentForm, RegForm, LoginForm
from blog.models import *


logger = logging.getLogger('blog.views')

# Create your views here.
def global_settings(request):
    #站点基本信息
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    # 分类信息获取
    category_list = Category.objects.all()
    # 归档
    archive_list = Article.objects.distinct_date()
    #标签云
    tag_list = Tag.objects.all()
    #友情链接
    links_list = Links.objects.all()
    #广告
    ad_list = Ad.objects.all()
    #文章浏览排行
    article_click_count_list = Article.objects.order_by("-click_count")[:6]
    #站长推荐排名
    article_is_recommend_list = Article.objects.order_by("-is_recommend")[:6]

    # 文章评论排行,annotate是聚合函数
    comment_count_list = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')#倒序排列，多在前少在后
    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list][:6]


    return locals()

def index(request):
    try:

        #广告轮播

        #最新文章数据
        article_list = getPage(request, Article.objects.all())


    except Exception as e:
        logger.error(e) #写入到日志
    return render(request, 'index.html',locals())

def archive(request):
    try:

        # 先获取客户端提交的信息
        year = request.GET.get('year',None)
        month = request.GET.get('month',None)

        article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)#模糊查询
        article_list = getPage(request,article_list)

    except Exception as e:
        logger.error(e)
    return render(request,'archive.html',locals())
#分页代码
def getPage(request,article_list):
    paginator = Paginator(article_list, 4)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except(EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)  # 用户输错就显示第一页
    return article_list
#文章详情
def article (request):
    try:
        # 获取文章id
        id = request.GET.get('id',None)

        try:
            #获取文章信息
            article = Article.objects.get(pk=id)
            # 阅读量 +1
            article.increase_views()
        except Article.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到对应的文章'})
        # 评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': id} if request.user.is_authenticated() else{'article': id})
        # 获取评论信息
        comments = Comment.objects.filter(article=article).order_by('id')
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)
    except Exception as e:
        print(e)
        logger.error(e)
    return render(request, 'article.html', locals())

#提交评论
def comment_post(request):
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            #获取表单信息
            comment = Comment.objects.create(username = comment_form.cleaned_data['author'],
                                             email = comment_form.cleaned_data['email'],
                                             url = comment_form.cleaned_data['url'],
                                             content = comment_form.cleaned_data['comment'],
                                             article_id = comment_form.cleaned_data['article'],
                                             user = request.user if request.user.is_authenticated() else None)
            comment.save()
        else:
            return render(request,'failure.html',{'reason': comment_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])


#注册
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                # 注册
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                    email=reg_form.cleaned_data["email"],
                                    url=reg_form.cleaned_data["url"],
                                    password=make_password(reg_form.cleaned_data["password"]),)
                user.save()

                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())

# 登录
def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())

#注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        print(e)
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

#分类
def category(request):
    try:
        # 先获取客户端提交的信息
        cid = request.GET.get('cid', None)
        try:
            category = Category.objects.get(pk=cid)
        except Category.DoesNotExist:
            return render(request, 'failure.html', {'reason': '分类不存在'})
        article_list = Article.objects.filter(category=category)
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'category.html', locals())

# 按标签查询对应的文章列表
def tag(request):
    try:
        # 先获取客户端提交的信息
        cid = request.GET.get('id', None)
        try:
            tag = Tag.objects.get(pk=cid)
        except Tag.DoesNotExist:
            return render(request, 'failure.html', {'reason': '标签不存在'})
        article_list = tag.article_set.all()
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'tag.html', locals())


#关于
def about(request):
    try:
        pass
    except Exception as e:
        print(e)
        logger.error(e)
    return render(request,'about.html',locals())


#联系
def contact(request):
    try:
        pass
    except Exception as e:
        print(e)
        logger.error(e)
    return render(request,'contact.html',locals())







