from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class CustomUser(AbstractUser):
    # Add any custom fields here, such as profile picture, phone number, etc.
    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Unique related_name
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups"
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Unique related_name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions"
    )
    pass

from django.db import models
from django.conf import settings

class Profile_models_viewlso(models.Model):
    user  = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    bio = models.TextField(blank = True, null= True)
    trader_type = models.CharField(
        max_length=34,
       choices = [('crypto', 'edrert'), ('dfsr', 'cypro')],
       blank= True,
       null=True

    )
    cypto_coins = models.CharField(max_length=435, blank=True,null=True)
    forex_accouny_type = models.CharField(max_length=54, blank=True, null=True)
    #_- we need to the account type for the charFiled as max_legth of 34, blank and null

# from django.db import models
# from django.conf import settings  # Import settings to use AUTH_USER_MODEL

# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Updated to use AUTH_USER_MODEL
#     bio = models.TextField(blank=True, null=True)
#     trader_type = models.CharField(
#         max_length=20, 
#         choices=[('crypto', 'Crypto'), ('forex', 'Forex'), ('other', 'Other')], 
#         blank=True, 
#         null=True
#     )
#     crypto_coins = models.CharField(max_length=255, blank=True, null=True)
#     forex_account_type = models.CharField(max_length=50, blank=True, null=True)
from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    trader_type = models.CharField(
        max_length=20,
        choices=[('crypto', 'Crypto'), ('forex', 'Forex'), ('other', 'Other')],
        blank=True,
        null=True
    )
    crypto_coins = models.CharField(max_length=255, blank=True, null=True)
    forex_account_type = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # Add this line

#-trader operations
from django.db import models

from django.conf import settings  # Import settings to use AUTH_USER_MODEL
from django.db import models

from django.contrib.auth.models import User

from django.conf import settings
from django.db import models

class Trade(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Ensure this is correct
    coin_name = models.CharField(max_length=50)
    trade_type = models.CharField(max_length=10)
    price_at_trade = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=4)
    trade_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.coin_name}"


from django.db import models
class PerformanceMetrics(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    total_return = models.FloatField(default=0)
    max_drawdown = models.FloatField(default=0)
    sharpe_ratio = models.FloatField(default=0)

# class Trade(models.Model):
#     trade_id = models.AutoField(primary_key=True)
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,  # Use AUTH_USER_MODEL instead of 'auth.User'
#         on_delete=models.CASCADE
#     )
#     coin_name = models.CharField(max_length=50)
#     trade_type = models.CharField(max_length=10, choices=[('buy', 'Buy'), ('sell', 'Sell')])
#     quantity = models.FloatField()
#     price_at_trade = models.FloatField()
#     trade_time = models.DateTimeField(auto_now_add=True)
#     profit_loss = models.FloatField(default=0.0)  # Auto-calculated later

#     def __str__(self):
#         return f"{self.user.username} - {self.coin_name} - {self.trade_type}"

# from django.db import models
# from django.conf import settings

# class PerformanceMetrics(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     metric_name = models.CharField(max_length=255)
#     metric_value = models.FloatField()
#     created_at = models.DateTimeField(auto_now_add=True)

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
