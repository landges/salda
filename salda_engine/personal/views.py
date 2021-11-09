from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from .forms import SignUpForm, ReviewForm
from django.contrib.auth.models import User
from market.models import Order,Status
from django.core.paginator import Paginator
from .models import *

# Create your views here.
def signout(request):
	logout(request)
	return redirect("main")

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


class SignUp(View):
	def get(self,request):
		form = SignUpForm()
		return render(request,'registration/signup.html',context={"form":form})

	def post(self,request):
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=user.username, password=raw_password)
			login(request, user)
			return redirect("main")
		else:
			return redirect("signup")


class Personal(View):
	def get(self,request):
		return render(request,'personal/personal.html')

class MyOrders(View):
	def get(self,request):
		user = User.objects.get(username=request.user)
		orders = Order.objects.filter(user=user).order_by('-created')
		return render(request,'personal/myorders.html',context={"orders":orders})

class OrderDetail(View):
	def get(self,request,pk):
		order = Order.objects.get(id=pk)
		return render(request,'personal/order_detail.html',context={"order":order})

class CancelOrder(View):
	def get(self,request,pk):
		order = Order.objects.get(id=pk)
		return render(request,'personal/cancel_order.html',context={"order":order})

	def post(self,request,pk):
		order = Order.objects.get(id=pk)
		text_cancel = request.POST.get("cancel")
		order.cancel = text_cancel
		order.status = Status.objects.get(id=2)
		order.save()
		return redirect("myorders")

class ReviewsView(View):
	def get(self,request):
		reviews = Review.objects.all().order_by('-created')
		for re in reviews:
			re.mark = list(range(re.mark))
		show_all = request.GET.get("SHOWALL_1",0)
		if show_all == 0:
			(page, is_paginated, prev_url, next_url) = pagination(request, reviews, 1)
		else:
			(page, is_paginated, prev_url, next_url) = pagination(request, reviews, len(reviews))
			is_paginated=True
		return render(request,'personal/reviews.html',context={"reviews":page,'is_paginated': is_paginated,
                   'next_url': next_url,
                   'prev_url': prev_url})

	def post(self,request):
		form = ReviewForm(request.POST)
		print(request.POST)
		form.instance.user = User.objects.get(username=request.user)
		if form.is_valid():
			form.save()
		return redirect("reviews")