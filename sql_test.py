import os
import django

# 设置Dango运行时需要的环境变量DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'First_project.settings')

# 加载Django的设置
django.setup()

# 导入模型，注意必须在加载完Django的设置后下面的这句导入模型语句才能被正确执行
from login.models import Account

# 创建一个用户
account = Account(username="spchara",password="123",gender=0)
account.save()
