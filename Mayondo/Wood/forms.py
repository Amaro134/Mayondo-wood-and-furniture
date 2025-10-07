from django import forms
from .models import Stock, Sales, Add_user
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

# ---------------- Add User Forms ----------------
class Add_userForm(UserCreationForm):
    class Meta:
        model = Add_user
        fields = ["username", "email", "role", "password1", "password2"]

    username = forms.CharField(error_messages={"required": "Username is required."})
    email = forms.EmailField(error_messages={"required": "Email is required.", "invalid": "Please enter a valid email."})
    role = forms.ChoiceField(choices=Add_user.ROLE_CHOICES, error_messages={"required": "Your role is required."})
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) < 3:
            raise forms.ValidationError("Username must be at least 3 characters long.")
        return username


class Add_userAuthenticationForm(AuthenticationForm):
    username = forms.CharField(error_messages={"required": "Username is required."})
    password = forms.CharField(error_messages={"required": "Password is required."})


# ---------------- Sales Form ----------------
class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ["customer_name", "product", "quantity_sold", "payment_method", "transport_used", 
                  "product_price", "sales_agent", "total_amount", "date_of_sale"]

    def clean_quantity_sold(self):
        qty = self.cleaned_data.get("quantity_sold")
        if qty is None or qty <= 0:
            raise ValidationError("Quantity must be greater than 0.")
        return qty

    def clean_product_price(self):
        price = self.cleaned_data.get("product_price")
        if price is None or price <= 0:
            raise ValidationError("Product price must be greater than 0.")
        return price

    def clean_total_amount(self):
        total = self.cleaned_data.get("total_amount")
        if total is None or total <= 0:
            raise ValidationError("Total amount must be greater than 0.")
        return total


# ---------------- Stock Form ----------------
class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["product_name", "type_of_product", "costprice", "quantity",
                  "selling_price", "supplier_name", "quality", "color", "measurement"]

    def clean_product_name(self):
        name = self.cleaned_data.get("product_name")
        if len(name) < 3:
            raise ValidationError("Product name must be at least 3 characters long.")
        return name

    def clean_costprice(self):
        price = self.cleaned_data.get("costprice")
        if price is None or price <= 0:
            raise ValidationError("Cost price must be greater than 0.")
        return price

    def clean_quantity(self):
        qty = self.cleaned_data.get("quantity")
        if qty is None or qty <= 0:
            raise ValidationError("Quantity must be greater than 0.")
        return qty

    def clean_selling_price(self):
        price = self.cleaned_data.get("selling_price")
        if price is None or price <= 0:
            raise ValidationError("Selling price must be greater than 0.")
        return price


# class StockForm(forms.ModelForm):
#     class Meta:
#         model = Stock
#         fields = [
#             'product_name',
#             'type_of_product',
#             'cost_price',
#             'selling_price',
#             'quantity',
#             'supplier_name',
#             'quality',
# #         ]
#         widgets = {
#             'product_name': forms.TextInput(attrs={
#                 'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
#             }),
#             'type_of_product': forms.TextInput(attrs={
#                 'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
#             }),
           
#             'costprice': forms.NumberInput(attrs={
#                  'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
#     }),

#             'selling_price': forms.NumberInput(attrs={
#                 'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
#             }),
#             'quantity': forms.NumberInput(attrs={
#                 'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
#             }),
#             'supplier_name': forms.TextInput(attrs={
#                 'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
#             }),

#             'quality': forms.TextInput(attrs={
#                 'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
#             }),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         cost_price = cleaned_data.get('cost_price')
#         selling_price = cleaned_data.get('selling_price')
#         quantity = cleaned_data.get('quantity')

#         if cost_price is not None and cost_price <= 0:
#             self.add_error('cost_price', 'Cost price must be greater than zero.')

#         if selling_price is not None and selling_price <= 0:
#             self.add_error('selling_price', 'Selling price must be greater than zero.')

#         if quantity is not None and quantity <= 0:
#             self.add_error('quantity', 'Quantity must be greater than zero.')

#         return cleaned_data
