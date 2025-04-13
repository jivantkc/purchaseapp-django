from django.contrib import admin
from .models import *
from payroll.models import *
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display =( 'name','user')
    list_filter = ('user',)
admin.site.register(Category,CategoryAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display= ("name",'user')
    list_filter = ('user',)
admin.site.register(Payment, PaymentAdmin)

class SupplierAdmin(admin.ModelAdmin):
    list_display=('user','name')
    list_filter = ('user',)
admin.site.register(Supplier, SupplierAdmin)

class DailypurchaseAdmin(admin.ModelAdmin):
    list_filter = ('user',)
    list_display=('user','date', 'suppliers', 'purchase', 'category', 'amount', 'payment',)
admin.site.register(Dailypurchase,DailypurchaseAdmin)

class CreditorsAdmin(admin.ModelAdmin):
    list_display=('user','name','type','amount')
    list_filter = ('user',)
admin.site.register(Creditors, CreditorsAdmin)


class OtherExpCategoryAdmin(admin.ModelAdmin):
    list_display=('user','name')
    list_filter = ('user',)
admin.site.register(OtherExpCategory, OtherExpCategoryAdmin)

class FixedExpenseAdmin(admin.ModelAdmin):
    list_display=('user','date','creditors','category','expensedetails','amount')
    list_filter = ('user',)
admin.site.register(FixedExpense, FixedExpenseAdmin)

 