from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls'), name='authentication'),
    path('social_auth/', include(('social_auth.urls', 'social_auth'),namespace="social_auth")),
    path('api/expenses/', include('expenses.urls'), name='expenses'),
    path('api/income/', include('income.urls'), name='income'),
    path('api/userstats/', include('stats.urls'), name='userstats'),
]
