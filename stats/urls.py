from stats import views
from django.urls import path

urlpatterns = [
    path('expense-summary-data', views.ExpenseSummaryStats.as_view(), name='expense-summary'),
    path('income-summary-data', views.IncomeSourcesSummaryStats.as_view(), name='income-summary'),
]