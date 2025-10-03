# from django import forms
# from .models import Stock, Sales, Add_user

# class Add_userForm(forms.ModelForm):
#     name = forms.CharField(error_messages={"required": "name is required."})
#     email = forms.EmailField(error_messages={"required": "Email is required."})
#     role = forms.CharField(error_messages={"required": "your role is required."})
#     password = forms.CharField(error_messages={"required": "Please enter your password."})
    
#     class Meta:
#         model = Add_user
#         fields = ["name", "email", "role", "password"]

# class SalesForm(forms.ModelForm):
#     product = forms.CharField(error_messages={"required": "please enter the product name"})
#     quantity = forms.IntegerField(error_messages={"required": "please enter the quantity required"})
#     payment_method = forms.CharField(error_messages={"required": "please enter the payment method"})
#     transport_used = forms.CharField(error_messages={"required": "please enter the transport means used"})
#     date_of_sale = forms.DateField(error_messages={"required": "please enter the correct date"})
#     product_price = forms.DecimalField(error_messages={"required": "please enter the product_price"})
#     sales_agent = forms.CharField(error_messages={"required": "please enter the name of the sales agent"})
#     total_amount = forms.DecimalField(error_messages={"required": "please enter the total amount of the sales made"})

#     class Meta:
#         model = Sales
#         fields = ["product", "quantity", "payment_method","transport_used", "date_of_sale", "product_price", "sales_agent", "total_amount" ]


# class StockForm(forms.ModelForm):
#     product_name = forms.CharField(error_messages={"required": "please enter the product name"})
#     type_of_product = forms.CharField(error_messages={"required": "please input the product type"})
#     costprice = forms.DecimalField(error_messages={"required": "please note down the costprice"})
#     quantity = forms.IntegerField(error_messages={"required":"please enter the quantity"})
#     selling_price = forms.DecimalField(error_messages={"required": "please enter the selling price"})
#     date_added = forms.DateField(error_messages={"required": "please feed in the date"})
#     quality = forms.CharField(error_messages={"required": "please enter the quality of the product"})
#     color = forms.CharField(error_messages={"required": "please enter the color of product"})
#     measurement = forms.CharField(error_messages={"required": "please enter the measurements"})

#     class Meta:
#         model = Stock
#         fields = ["product_name", "type_of_product", "costprice", "quantity", 
#                   "selling_price", "supplier_name", "date_added", 
#                   "quality", "color", "measurement"]
