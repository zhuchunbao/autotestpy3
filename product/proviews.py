from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django. shortcuts import render
from product.models import Product
#产品管理
def product_manage(request):
    username = request.session.get('user', '')
    product_list = Product.objects.all()
    return render(request, "product_manage.html", {"user": username,"products": product_list})
# 搜索功能
@login_required
def productsearch(request):
    username = request.session.get('user', '') # 读取浏览器登录 Session
    search_productname = request.GET.get("productname", "")
    product_list = Product.objects.filter(productname__icontains=search_productname)
    return render(request,'product_manage.html', {"user": username,"products":product_list})