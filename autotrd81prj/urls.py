"""autotrd81prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from autotrd81app.views import upload_trade, list_trade, getChartImage, newSingleTrade, IndexView, newCrossTrade, TradeListView, getMultiChartImage 

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('upload_trade/', upload_trade, name="upload_trade"),
    path('list_trade/', list_trade, name="list_trade"),
    path('<str:strat>/<str:inSym>/getChartImage/', getChartImage, name="getChartImage"),
    path('getMultiChartImage/', getMultiChartImage, name="getMultiChartImage"),
    path('<str:strat>/<str:transType>/newSingleTrade/', newSingleTrade, name="newSingleTrade"),
    path('<str:strat>/newCrossTrade/', newCrossTrade, name="newCrossTrade"),
    path('insertKiteTrades/', TradeListView.as_view(), name="insertKiteTrades"),
]

