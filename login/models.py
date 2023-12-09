from django.db import models

# Create your models here.
class Account(models.Model):
    # 用户名 str类
    username = models.CharField(max_length=20, verbose_name='用户名')
    # 密码 str类
    password = models.CharField(max_length=20, verbose_name='密码')
    # 性别 int类
    gender = models.IntegerField(default=0, verbose_name='性别')