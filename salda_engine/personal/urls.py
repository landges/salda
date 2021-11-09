from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
	path('signout/',signout,name='signout'),
	path('signup/',SignUp.as_view(),name="signup"),
	path('personal/',Personal.as_view(),name="personal"),
	path('orders/',MyOrders.as_view(),name="myorders"),
	path('orders/<int:pk>/',OrderDetail.as_view(),name="order_detail"),
	path('cancelorder/<int:pk>/',CancelOrder.as_view(),name="cancelorder"),
	path('reviews/',ReviewsView.as_view(), name="reviews"),
]