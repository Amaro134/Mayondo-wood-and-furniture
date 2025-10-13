from django import forms
from .models import Stock, Sales, Add_user
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

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

class Add_userAuthenticationForm(forms.Form):
    username = forms.CharField(error_messages={"required": "Username is required."})
    password = forms.CharField(error_messages={"required": "Password is required."})

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password: 
            print(f"username: {username}")
            print(f"password: {password}")
            user = authenticate(username=username, password=password)
            print(f"User details: {user}")
            
            # Debugging the result of authenticate()
            if user is None:
                raise forms.ValidationError("Please enter correct credentials.")

            # If authenticate() works, add user to cleaned_data for further use
            cleaned_data["user"] = user
        else:
            raise forms.ValidationError("Both username and password are required.")  # In case one of them is missing

        return cleaned_data

# class Add_userAuthenticationForm(forms.Form):
#     username = forms.CharField(error_messages={"required": "Username is required."})
#     password = forms.CharField(error_messages={"required": "Password is required."})

#     def clean(self):
#         cleaned_data = super().clean() 
#         username = cleaned_data.get("username")
#         password = cleaned_data.get("password")
#         print(f"username: {username}")
#         print(f"password: {password}")

#         if username and password: 
#             print(f"username: {username}")
#             print(f"password: {password}")

#             user = authenticate(username=username, password=password)
#             print(f"User details: {user}")
#             if user is None: 
#                 raise forms.ValidationError("please enter your correct credentials.")
#             cleaned_data["user"] = user
#         return cleaned_data

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



