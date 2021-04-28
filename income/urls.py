from django.urls import path
from .import views

urlpatterns = [
    path('', views.ListIncomApiView.as_view(), name='income'),
    path('<int:id>', views.UpdateIncomeApiView.as_view(), name='income-detail')
]