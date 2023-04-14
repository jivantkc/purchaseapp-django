from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE )
    name=models.CharField(max_length=100)
    def __str__(self):
    	return self.name

class Payment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE )
    name=models.CharField(max_length=100)
    def __str__(self):
    	return self.name
# Create your models here.
class Supplier(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE )
    name=models.CharField(max_length=100)
    category=models.ForeignKey(Category, on_delete=models.CASCADE )
    def __str__(self):
    	return self.name

# Create your models here.
class Dailypurchase(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE )
    date=models.DateField()
    suppliers=models.ForeignKey(Supplier, on_delete=models.CASCADE)
    purchase=models.CharField(max_length=100)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    amount=models.FloatField()
    payment=models.ForeignKey(Payment, on_delete=models.CASCADE)
    def __str__(self):
        	return self.suppliers.name




"""
To send email in forget password
"""

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Purchase App"),
        # message:
        "Some one requested for password reset, please click link to reset password. " "http://127.0.0.1:8000%s"%email_plaintext_message,
        # from:
        "noreply@blackwood.com.hk",
        # to:
        [reset_password_token.user.email]
    )