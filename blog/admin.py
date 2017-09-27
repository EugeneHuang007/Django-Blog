from django.contrib import admin
from blog.models import *
# Register your models here.

#自定义articleadmin的内容
class ArticleAdmin(admin.ModelAdmin):

    list_display = ('title','desc','click_count',)#显示哪些列
    list_display_links = ('title','desc')#附上链接
    list_editable = ('click_count',)#点击次数

    fieldsets = (
        (None,{
            'fields':('title','desc','content','user','tag','category','article_cover')
        }),
        ('高级设置',{
            'classes':('collapse',),
            'fields':('click_count','is_recommend',)
        })
    )
    class Media:
        js = (
            '/static/js/kindeditor-4.1.10/kindeditor.js',
            '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.10/config.js'
        )

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)
