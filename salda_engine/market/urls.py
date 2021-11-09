from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('main/',MainPage.as_view(),name="main"),
    path('service/', Service.as_view(),name="service"),
    path('catalog/', Catalog.as_view(),name="catalog"),
    path('catalog/<str:cat>/',ProductList.as_view(),name="products"),
    path('catalog/<str:cat>/<int:pk>/',ProductDetail.as_view(),name="product_detail"),
    path('upload/',upload_csv,name="upload"),
    path('card/',Card.as_view(),name="card"),
    path('order/',OrderView.as_view(),name="order"),
    path('news/',NewsList.as_view(),name="news_list"),
    path('news/<str:slug>/',NewsDetail.as_view(),name="news_detail"),
    path('contacts/',Contacts.as_view(),name="contacts"),
    path('dokumentatsiya/',Documents.as_view(),name="docs"),
    path('search/',search,name="search"),

]
