from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model  # Make sure this is imported


from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']  # Add any fields you need

    password = forms.CharField(widget=forms.PasswordInput())

class LoginForm(AuthenticationForm):
    pass

# from django import forms
# from .models import Profile

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['bio', 'trader_type', 'crypto_coins', 'forex_account_type']
#         widgets = {
#             'bio': forms.Textarea(attrs={'rows': 4}),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         trader_type = cleaned_data.get('trader_type')
#         crypto_coins = cleaned_data.get('crypto_coins')
#         forex_account_type = cleaned_data.get('forex_account_type')

#         if trader_type == 'crypto' and not crypto_coins:
#             self.add_error('crypto_coins', 'Please specify the coins you are interested in.')
#         elif trader_type == 'forex' and not forex_account_type:
#             self.add_error('forex_account_type', 'Please select your forex account type.')

#         return cleaned_data
from django import forms
from .models import Profile
#- profile form 
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'trader_type', 'crypto_coins', 'forex_account_type', 'profile_image']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        trader_type = cleaned_data.get('trader_type')
        crypto_coins = cleaned_data.get('crypto_coins')
        forex_account_type = cleaned_data.get('forex_account_type')

        if trader_type == 'crypto' and not crypto_coins:
            self.add_error('crypto_coins', 'Please specify the coins you are interested in.')
        elif trader_type == 'forex' and not forex_account_type:
            self.add_error('forex_account_type', 'Please select your forex account type.')

        return cleaned_data
        



#_ for the profileFormatting 


# class Profiel_foriming_artibutes(forms.modelformset_factory):
#     class Meta:
#         model = Profile
#         fields = ['bio', 'tradere_type', 'crypto_coi', 'forex_accounts']
#         widgetsa = {
#             'bio' : forms.Textarea(attrs={'rows':4}),
#         }
#         sawtrer = ['textFiled', 'memeCoins', 'indexs', 'sharts']
#         wdsa = {
#             'cnalds': forms.Textarea(attrs={'rows': 45}),

#         }




from django import forms
from .models import Trade

class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ['price_at_trade', 'quantity', 'coin_name', 'trade_type']  # Fields in the model
