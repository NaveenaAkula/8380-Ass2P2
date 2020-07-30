from django.db import models
from django.utils import timezone
import requests

# Create your models here.
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    cust_number = models.IntegerField(blank=False, null=False)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    email = models.EmailField(max_length=200)
    cell_phone = models.CharField(max_length=50)
    created_date = models.DateTimeField(
        default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.cust_number)


class Investment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='investments')
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    acquired_value = models.DecimalField(max_digits=10, decimal_places=2)
    acquired_date = models.DateField(default=timezone.now)
    recent_value = models.DecimalField(max_digits=10, decimal_places=2)
    recent_date = models.DateField(default=timezone.now, blank=True, null=True)

    def created(self):
        self.acquired_date = timezone.now()
        self.save()

    def updated(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.customer)

    def results_by_investment(self):
        return self.recent_value - self.acquired_value


class Stock(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='stocks')
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    shares = models.DecimalField(max_digits=10, decimal_places=1)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(default=timezone.now, blank=True, null=True)

    def created(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.customer)

    def initial_stock_value(self):
        return self.shares * self.purchase_price

    # @cache_page(3600)
    def current_stock_price(self):
        symbol_f = str(self.symbol)
        main_api = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='
        api_key = '&interval=1min&apikey=DIEHSUTDE76KU073'
        url = main_api + symbol_f + api_key
        json_data = requests.get(url).json()
        open_price = float(json_data["Global Quote"]["02. open"])
        share_value = open_price
        return share_value

    def current_stock_value(self):
        return float(self.current_stock_price()) * float(self.shares)

    def currency_rate(self):
        main_api = 'https://free.currconv.com/api/v7/convert?q=INR_PHP&compact=ultra&apiKey=9d88d44ed0b4895bcb88'
        json_data = requests.get(main_api).json()
        value = float(json_data["INR_PHP"])
        return value


Categories = [("Equity Funds", "Equity Funds"), ("Bond Funds", "Bond Funds"),
              ("Money Market Funds", "Money Market Funds")]


class MutualFund(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='mutualfunds')
    category = models.CharField(max_length=50, choices=Categories)
    description = models.CharField(max_length=200)
    acquired_value = models.DecimalField(max_digits=10, decimal_places=2)
    acquired_date = models.DateField(default=timezone.now)
    recent_value = models.DecimalField(max_digits=10, decimal_places=2)
    recent_date = models.DateField(default=timezone.now, blank=True, null=True)

    def created(self):
        self.acquired_date = timezone.now()
        self.save()

    def updated(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.customer)
