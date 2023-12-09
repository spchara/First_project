from django.shortcuts import render, HttpResponse, redirect
from login import models

# Create your views here.
def login(request):
    if request.method == "GET":
        request.session.delete('is_login')
        request.session.delete('user')
        return render(request, "login.html")

    # 获取输入的数据
    username = request.POST.get("username")
    pwd = request.POST.get("pwd")
    agreement = request.POST.get("agreement")

    # 判断是否同意协议
    if agreement != "Yes":
        return render(request, "login.html", {"error_msg": "请阅读并同意服务协议与隐私保护指引"})

    # 读取数据库
    user_list_obj = models.Account.objects.all()
    user_list = []
    for account in user_list_obj:
        user_list.append((account.username, account.password))

    # 判断账号和密码正确
    if (username, pwd) not in user_list:
        return render(request, "login.html", {"error_msg": "账号或密码错误"})

    # 保存session
    request.session.set_expiry(3600)
    request.session['username'] = username
    request.session['is_login'] = True
    return redirect("/index/", {'login_static': '欢迎你，' + username})


def index(request):
    if request.session.get('is_login', None):
        return render(request, 'index.html', {'login_static': '欢迎你' + request.session['username']})
    else:
        return redirect("/index/login/")


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    # 获取输入
    username = str(request.POST.get("username"))
    pwd = str(request.POST.get("pwd"))
    conf_pwd = str(request.POST.get("conf_pwd"))
    phone_num = str(request.POST.get("phone_number"))
    sex = request.POST.get("sex")
    agreement = str(request.POST.get("agreement"))

    # 判断是否同意协议
    if agreement != "Yes":
        return render(request, "register.html", {"error_msg": "请阅读并同意服务协议与隐私保护指引"})
    # 判断用户名是否合法
    cha = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)] + ['_'] + [str(i) for i in range(10)]
    for i in username:
        if i not in cha:
            return render(request, "register.html", {"error_msg": "用户名只能由字母、数字及下划线组成"})
    # 判断用户名是否已经被使用
    user_list_obj = models.Account.objects.all()
    for account in user_list_obj:
        if username == account.username:
            return render(request, "register.html", {"error_msg": "该用户名已存在"})
    # 判断密码是否合法
    if len(pwd) > 20 or len(pwd) < 6:
        return render(request, "register.html", {"error_msg": "密码长度须在6-20位之间"})
    if pwd != conf_pwd:
        return render(request, "register.html", {"error_msg": "两次输入的密码不一致！"})
    for i in pwd:
        if '\u4e00' <= i <= '\u9fa5':
            return render(request, "register.html", {"error_msg": "密码中不能包含中文！"})

    # 将账号信息写入数据库
    models.Account.objects.create(username=username, password=pwd, gender=sex)
    return redirect("/index/login/")

#
# def db_handle():
#     pass
