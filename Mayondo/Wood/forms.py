from django import forms
from .models import Stock, Sales, Add_user
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class Add_userForm(UserCreationForm):
    class Meta:
        model = Add_user
        fields = ["username", "email", "role", "password"]
        username = forms.CharField(error_messages={"required": "username is required."})
        email = forms.EmailField(error_messages={"required": "Email is required.", 
                                                 
                                                 'invaild': 'please enter a vaild email'})
        
        role = forms.CharField(error_messages={"required": "your role is required."})
        password = forms.CharField(error_messages={"required": "Please enter your password."})
    
    def clean_name(self):
        username = self.cleaned_data["username"]
        if len(username) < 3:
            raise forms.ValidationError("please enter a username that is more than 3 characters")
        return username 
class Add_userAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invaild_login": "Please enter the right credentials"
    }        
    username = forms.CharField(error_messages={"required": "username is required."})
    email = forms.EmailField(error_messages={"required": "Email is required.",}) 

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ["product", "quantity", "payment_method","transport_used", "product_price", "sales_agent", "total_amount" ]

        product = forms.CharField(error_messages={"required": "please enter the product name"})
        quantity = forms.IntegerField(error_messages={"required": "please enter the quantity required"})
        payment_method = forms.CharField(error_messages={"required": "please enter the payment method"})
        transport_used = forms.CharField(error_messages={"required": "please enter the transport means used"})
       
        product_price = forms.DecimalField(error_messages={"required": "please enter the product_price"})
        sales_agent = forms.CharField(error_messages={"required": "please enter the name of the sales agent"})
        total_amount = forms.DecimalField(error_messages={"required": "please enter the total amount of the sales made"})

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity <= 0:
            raise forms.ValidationError("quantity must be above 0")
        return quantity 
    def clean_product_price(self):
        product_price = self.cleaned_data["product_price"]
        if product_price < 5000:
            raise forms.ValidationError("product_price must be 5000 and above")
        
        return product_price    

   

class StockForm(forms.ModelForm):
    product_name = forms.CharField(error_messages={"required": "please enter the product name"})
    type_of_product = forms.CharField(error_messages={"required": "please input the product type"})
    costprice = forms.DecimalField(error_messages={"required": "please note down the costprice"})
    quantity = forms.IntegerField(error_messages={"required":"please enter the quantity"})
    selling_price = forms.DecimalField(error_messages={"required": "please enter the selling price"})
    date_added = forms.DateField(error_messages={"required": "please feed in the date"})
    quality = forms.CharField(error_messages={"required": "please enter the quality of the product"})
    color = forms.CharField(error_messages={"required": "please enter the color of product"})
    measurement = forms.CharField(error_messages={"required": "please enter the measurements"})

    class Meta:
        model = Stock
        fields = ["product_name", "type_of_product", "costprice", "quantity", 
                  "selling_price", "supplier_name", "date_added", 
                  "quality", "color", "measurement"]
