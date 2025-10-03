from django.db import models

# Create your models here.
class Login(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)
class Sales(models.Model):
    PAYMENT_CHOICES = [
        ("Cash", "Cash"),
        ("Cheque", "Cheque"),
        ("Bank overdraft", "Bank overdraft"),
    ]

    TRANSPORT_CHOICES = [
        ("Company_provision", "Company provision"),
        ("Self_provision", "Self provision"),
    ]

    customer_name = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    quantity_sold = models.IntegerField()
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_CHOICES,
        blank=True
    )
    transport_used = models.CharField(
        max_length=50,
        choices=TRANSPORT_CHOICES,
        blank=True
    )
    date_of_sale = models.DateField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    sales_agent = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale to {self.customer_name} on {self.date_of_sale}"



class Stock(models.Model):
    product_name = models.CharField(max_length=100)
    type_of_product = models.CharField(max_length=100)
    costprice = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier_name = models.CharField(max_length=100)
    date_added = models.DateField()
    quality = models.CharField(max_length=100)
    color = models.CharField(max_length=50, default="blue")
    measurement = models.CharField(max_length=50, default="0 metres")
    
    def __str__(self):
        return str(self.product_name)
    
    
class Add_user(models.Model):
    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Manager", "Manager"),
        ("Sales Agent", "Sales Agent"),
    ]    
    name = models.CharField(max_length=100)
    email = models.CharField(unique=True)
    password = models.CharField(max_length=100) 
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Sales Agent")

    def __str__(self):
        return str (self.name)   