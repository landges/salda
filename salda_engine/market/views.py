from django.shortcuts import render,redirect
import pandas as pd
from .models import *
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.db.models import Q
import json
from django.http import JsonResponse
from .forms import OrderForm
from django.core.paginator import Paginator
import ast

def pagination(request, objects_list, count_of_page):
    paginator = Paginator(objects_list, count_of_page)
    page_number = request.GET.get('PAGEN_1', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = 'PAGEN_1={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = 'PAGEN_1={}'.format(page.next_page_number())
    else:
        next_url = ''
    return (page, is_paginated, prev_url, next_url)

# Create your views here.
def upload_csv(request):
	df = pd.read_csv('scrap/data_2.csv',delimiter="&")
	df.columns=["name","slug","cat","price","dsc","article","have_flag","stats","img"]
	# slugs = df['slug'].unique()
	# names = df['cat'].unique()
	# for sl,name in zip(slugs,names):
	# 	cat = Category(name=name,slug=sl)
	# 	cat.save()
		# 	df = pd.read_csv('scrap/new_data_2.csv',delimiter=";")
		# df.columns=["id","name", "slug", "cat", "price", "dsc", "article", "have_flag", "is_new", "stats", "img"]
		# for index,row in df.iterrows():
		# 	pr= Product.objects.filter(name=row['name']).first()
		# 	if pr is None:
		# 		continue
		# 	else:
		# 		print(pr)
		# 		stats = ast.literal_eval(row['stats'])
		# 		pr.stats = stats
		# 		pr.save()
	for index, row in df.iterrows():
		category = Category.objects.get(name=row['cat'])
		image_path = 'scrap/' + row['img'].replace('\\','/')
		pr= Product.objects.filter(name=row['name']).first()
		if pr is None:
			p = Product(name=row['name'],alter_category=category, price=float(row['price']),dsc=row['dsc'],article=row['article'], in_storage=bool(row['have_flag']),stats=row['stats'],img=image_path)
			p.save()
		else:
			pr.alter_category = category
			pr.save()

class MainPage(View):
	def get(self,request):
		main=True
		products = Product.objects.all()[:20]

		# for p in products:
		# 	s=str(p.stats)
		# 	p.stats = s.replace('\\','')
		# 	p.save()
		return render(request,'market/main.html',context={"main":main,"products":products})

	def post(self,request):
		print('ffff')
		page_number=request.POST.get('page')
		products = Product.objects.all()
		paginator = Paginator(products, 20)
		page = paginator.get_page(page_number)
		return render(request,'market/ajax_load.html',context={"products":page})


class Service(View):
	def get(self,request):
		categories = Category.objects.filter(service=True)
		return render(request,'market/service.html',context={"categories":categories})

class Catalog(View):
	def get(self,request):
		categories = Category.objects.filter(service=False)
		return render(request,'market/catalog.html',context={"categories":categories})
		

class ProductList(View):
	def get(self,request,cat):
		products=Product.objects.filter(Q(category__slug=self.kwargs['cat'])|Q(alter_category__slug=self.kwargs['cat']))
		category = Category.objects.get(slug=cat)	
		(page, is_paginated, prev_url, next_url) = pagination(request, products, 20)
		return render(request,'market/product_list.html',context={"products":page,'is_paginated': is_paginated,
                   'next_url': next_url,
                   'prev_url': prev_url,
                   "category":category})



class ProductDetail(View):
	def get(self,request, cat, pk):
		product = Product.objects.get(id=pk)
		link_products=[]
		if product.alter_category:
			link_products = Product.objects.filter(alter_category = product.alter_category)[:10]
		return render(request,'market/product_detail.html',context={"product":product,"link_products":link_products})


	def post(self,request, cat, pk):
		return_dict = dict()
		session_key = request.session.session_key
		data = request.POST
		product_id = data.get("product_id")
		print(product_id)
		product = Product.objects.get(id=product_id)
		nmb = data.get("nmb")
		is_delete = data.get("is_delete")
		if is_delete == 'true':
			ProductInBasket.objects.filter(product=product).update(is_active=False)
		else:
			new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product=product,
																		is_active=True, defaults={"nmb": nmb})
			if not created:
				print("not created")
				new_product.nmb += int(nmb)
				new_product.save(force_update=True)

		# common code for 2 cases
		products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
		products_total_nmb = products_in_basket.count()
		return_dict["products_total_nmb"] = products_total_nmb

		return_dict["products"] = list()
		# for item in products_in_basket:
		# 	product_dict = dict()
		# 	product_dict["id"] = item.id
		# 	product_dict["name"] = item.product.name
		# 	product_dict["product_id"] = item.product.id
		# 	product_dict["price_per_item"] = item.price_per_item
		# 	product_dict["nmb"] = item.nmb
		# 	product_dict["href"] = item.product.id
		# 	product_dict["image"] = item.product.productimage_set.all()[0].path
		# 	return_dict["products"].append(product_dict)

		return JsonResponse(return_dict)


class Card(View):
	def get(self, request):
		return render(request,'market/basket.html')

	def post(self, request):
		print(request.POST)
		nmb_list = request.POST.getlist('product-nmb')
		session_key = request.session.session_key
		products_in_basket = ProductInBasket.objects.filter(session_key=session_key,is_active=True)
		for nmb, product in zip(nmb_list,products_in_basket):
			product.nmb = int(nmb)
			product.save()
		return redirect("card")

class OrderView(View):
	def get(self,request):
		order_id=request.GET.get('order_id','')
		if order_id !='':
			order = Order.objects.get(id=order_id)
			return render(request,'market/order_complite.html',context={"order":order})
		else:
			return render(request,'market/order.html')

	def post(self, request):
		print(request.POST)
		form = OrderForm(request.POST)
		if form.is_valid():
			user = User.objects.get(username=request.user)
			form.instance.user =user
			form.instance.status=Status.objects.get(id=1)
			order = form.save()

			session_key = request.session.session_key
			product_list = request.POST.getlist('product-id')
			for product_id in product_list:
				product_in_basket = ProductInBasket.objects.get(session_key=session_key,is_active=True, product_id=product_id)
				ProductInOrder.objects.create(product=product_in_basket.product, nmb=product_in_basket.nmb,
											price_per_item=product_in_basket.price_per_item,
											total_price=product_in_basket.total_price,
											order=order)
				product_in_basket.is_active=False
				product_in_basket.save()
			return redirect(f'/order/?order_id={order.id}')


class NewsList(ListView):
	model = News
	queryset = News.objects.all()


class NewsDetail(DetailView):
	model = News
	slug_field = "slug"


class Documents(ListView):
	model = Document

def search(request):
	q=request.POST.get('q')
	if not q:
		q = request.GET.get('q')
	order = request.GET.get('order','price')
	print(order)
	products = Product.objects.filter(dsc__icontains=q).order_by(order)
	(page, is_paginated, prev_url, next_url) = pagination(request, products, 10)
	return render(request,'market/search.html',context={"search_query":page,"q":q,'is_paginated': is_paginated,
                   'next_url': next_url,
                   'prev_url': prev_url,"order":order})

class Contacts(ListView):
	model = Market
