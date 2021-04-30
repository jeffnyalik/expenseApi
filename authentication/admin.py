from django.contrib import admin

from authentication.models import User
from income.models import Income
from expenses.models import Expense


admin.site.register(User)
admin.site.register(Income)
admin.site.register(Expense)
