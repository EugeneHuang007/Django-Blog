from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

#user,继承方式扩展用户信息
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m',default='avatar/default.png',max_length=200,verbose_name='头像')
    qq = models.CharField(max_length=20,blank=True,null=True,verbose_name='QQ号码')
    model = models.CharField(max_length=11,blank=True,null=True,unique=True,verbose_name='手机号码')
    url = models.URLField(max_length=100,blank=True,null=True,verbose_name='个人网页地址')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username

#tag
class Tag(models.Model):
    name=models.CharField(max_length=30,verbose_name='标签名称')

    class Meta:
        verbose_name='标签'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

#分类
class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField(default=999,verbose_name='分类的排序')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id'] #从小到大排序，要倒序的话index加个负号

    def __str__(self):
        return self.name

#自定义文章model的管理器
#1.新加一个数据处理的方法，2.改变原有的queryset  这里用的是方法1
class ArticleManager(models.Manager):
    def distinct_date(self):
        distinct_date_list = []    #保存结果的list
        date_list = self.values('date_publish')
        for date in date_list:
            date = date['date_publish'].strftime('%Y/%m')+'文章存档' #注意文字另外加入
            if date not in distinct_date_list:    #如果没有则添加
                distinct_date_list.append(date)
        return distinct_date_list


#文章模型
class Article(models.Model):
    title = models.CharField(max_length=50,verbose_name='文章标题')
    desc = models.CharField(max_length=50,verbose_name='文章描述')
    content = models.TextField(verbose_name='文章内容')
    click_count = models.PositiveIntegerField(default=0,verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False,verbose_name='是否推荐')
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    user = models.ForeignKey(User,verbose_name='用户')
    category = models.ForeignKey(Category,blank=True,null=True,verbose_name='分类')
    tag = models.ManyToManyField(Tag,blank=True,verbose_name='标签')
    article_cover = models.ImageField(upload_to='article_cover/%Y/%m',default='article_cover/default.png',max_length=900,verbose_name='文章封面')

    objects = ArticleManager() #把自定义的manger关联进来

#点击量计数
    def increase_views(self):
        self.click_count += 1
        self.save(update_fields=['click_count']) #用 update_fields只更新click_count，提高效率

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __str__(self):
        return self.title

#评论
class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    username = models.CharField(max_length=30,blank=True,null=True,verbose_name='用户名')
    email= models.EmailField(max_length=50,blank=True,null=True,verbose_name='邮箱地址')
    url = models.URLField(max_length=100,blank=True,null=True,verbose_name='个人网页地址')
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    user = models.ForeignKey(User,blank=True,null=True,verbose_name='用户')
    article = models.ForeignKey(Article,blank=True,null=True,verbose_name='文章')
    pid = models.ForeignKey('self',blank=True,null=True,verbose_name='父级评论')



    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']


    def __str__(self):
        return str(self.id)

#友情链接
class Links(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    description = models.CharField(max_length=200,verbose_name='友情链接描述')
    callback_url = models.URLField(verbose_name='url地址')
    data_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    index =models.IntegerField(default=999,verbose_name='排列顺序（从小到大）')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['index','id']


    def __str__(self):
        return self.title

#广告
class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name='广告标题')
    description = models.CharField(max_length=200, verbose_name='广告描述')
    image_url = models.ImageField(upload_to='ad/%Y%m',verbose_name='图片路径')
    callback_url = models.URLField(null=True,blank=True,verbose_name='回调URL')
    data_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    index = models.IntegerField(default=999,verbose_name='排列顺序（从小到大）')

    class Meta:
        verbose_name = u'广告'
        verbose_name_plural = verbose_name
        ordering = ['index','id']

    def __str__(self):
        return self.title














