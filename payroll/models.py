from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Creditors(models.Model):
    CREDITORS_TYPE_CHOICES = {
    "staff": "Staff",
    "rent": "Rent",
    "loan": "Loan",
    "other": "Other",
    }
 
    user=models.ForeignKey(User, on_delete=models.CASCADE )
    name=models.CharField(max_length=100)
    type=models.CharField(max_length=100, choices=CREDITORS_TYPE_CHOICES.items())
    amount=models.CharField(max_length=100)
    # category=models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True)
    def __str__(self):
    	return self.name
    
class OtherExpCategory(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE )
    name=models.CharField(max_length=100)
    def __str__(self):
    	return self.name
    
# Create your models here.
class FixedExpense(models.Model):
    user=models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True  )
    date=models.DateField()
    creditors=models.ForeignKey(Creditors, on_delete=models.DO_NOTHING, null=True)
    category=models.ForeignKey(OtherExpCategory, on_delete=models.DO_NOTHING, null=True)
    expensedetails=models.CharField(max_length=100)
    amount=models.FloatField()
     
    def __str__(self):
        	return self.expensedetails


