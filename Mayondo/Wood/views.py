from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Stock, Sales, Add_user
from datetime import datetime
from .forms import Add_userForm, SalesForm, StockForm, Add_userAuthenticationForm
from .forms import StockForm


# ---------------- Landing ----------------
def landingPage(request):
    return render(request, "index.html")

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # Here you would typically validate the username and password
        # For simplicity, let's assume any non-empty username and password is valid
        if username and password:
            return redirect("dashboard")  # Redirect to dashboard on successful login
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


# ---------------- Stock Views ----------------
# Show empty stock form
# def addStock(request):
#     if request.method == "POST":
#         form = StockForm(request.POST)
#         if form.is_valid():
#             form.save()  # saves Stock object
#             return redirect("stock_list")
#     else:
#         form = StockForm()

#     return render(request, "stock.html", {"form": form})
def addStock(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        type_of_product = request.POST.get("type_of_product")
        costprice = request.POST.get("cost_price")
        quantity = request.POST.get("quantity")
        selling_price = int(request.POST.get("selling_price"))
        supplier_name = request.POST.get("supplier_name")
        date_added = request.POST.get("date_added")
        quality = request.POST.get("quality")
        color = request.POST.get("color")
        measurement = request.POST.get("measurements")

        stock = Stock(
            product_name=product_name,
            type_of_product=type_of_product,
            costprice=costprice,
            quantity=quantity,
            selling_price=selling_price,
            supplier_name=supplier_name,
            date_added=date_added,
            quality=quality,
            color=color,
            measurement=measurement,
        )
        stock.save()
        return redirect("stock_list")
    return render(request, "stock.html")

def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, "stocklist.html", {"stocks": stocks})

# ---------------- Edit Stock ----------------
def stockedit(request, id):
    stock = get_object_or_404(Stock, id=id)

    if request.method == "POST":
        stock.product_name = request.POST.get("product_name")
        stock.type_of_product = request.POST.get("type_of_product")
        stock.costprice = request.POST.get("cost_price")
        stock.quantity = request.POST.get("quantity")
        stock.selling_price = request.POST.get("selling_price")
        stock.supplier_name = request.POST.get("supplier_name")
        stock.date_added = request.POST.get("date_added")
        stock.quality = request.POST.get("quality")
        stock.color = request.POST.get("color")
        stock.measurement = request.POST.get("measurements")

        stock.save()
        return redirect("stock_list")

    return render(request, "stockedit.html", {"selected": stock})



# View one stock item by ID
def stockview(request, id):
    stock = get_object_or_404(Stock, id=id)
    return render(request, "stockview.html", {"selected": stock})

def stockdelete(request, id):
    stock = get_object_or_404(Stock, id=id)
    if request.method == "POST":
        stock.delete()
        return redirect('stock_list')
    return render(request, "stockdelete.html", {"stock": stock})
 # make sure this matches your URL name

def stockupdate(request, id):
    stock = get_object_or_404(Stock, id=id)
    # Example: maybe you want to show a prefilled form
    return render(request, "stockedit.html", {"stock": stock})

# ---------------- Dashboard ----------------
def dashboard(request):
    # Get latest 5 stocks and sales
    stocks = Stock.objects.all().order_by('-date_added')[:5]
    sales = Sales.objects.all().order_by('-date_of_sale')[:5]

    # Summary calculations
    total_stock = Stock.objects.count()  # total products
    current_stock = Stock.objects.filter(quantity__gt=0).count()  # available products
    restock_value = sum(item.costprice * item.quantity for item in Stock.objects.all())  # total cost

    context = {
        "total_stock": total_stock,
        "current_stock": current_stock,
        "restock_value": restock_value,
        "stocks": stocks,
        "sales": sales,
    }

    return render(request, "dashboard.html", context)

# ---------------- Sales Views ----------------
# Handle sales form submission


def add_sales(request):
    if request.method == "POST":
        date_str = request.POST.get("date_of_sale")
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        sale = Sales(
            customer_name=request.POST.get("customer_name"),
            product=request.POST.get("product"),
            quantity_sold=int(request.POST.get("quantity_sold")),
            payment_method=request.POST.get("payment_method"),
            transport_used=request.POST.get("transport_used"),
            date_of_sale=date_obj,
            product_price=float(request.POST.get("product_price")),
            sales_agent=request.POST.get("sales_agent"),
            total_amount=float(request.POST.get("total_amount")),
        )
        sale.save()
        return redirect("sales_list") 
    else:
        sale = SalesForm()
    return render(request, "add_sales.html")


# List all sales
def sales_list(request):
    all_sales = Sales.objects.all()
    return render(request, "sales_list.html", {"sales": all_sales})

def salesedit(request, id):
    try:
        selected = Sales.objects.get(id=id)
    except Sales.DoesNotExist:
        return redirect("sales_list")

    if request.method == "POST":
        selected.customer_name = request.POST.get("customer_name")
        selected.product = request.POST.get("product")
        selected.quantity_sold = int(request.POST.get("quantity_sold"))
        selected.payment_method = request.POST.get("payment_method")
        selected.transport_used = request.POST.get("transport_used")
        selected.date_of_sale = datetime.strptime(request.POST.get("date_of_sale"), "%Y-%m-%d").date()
        selected.product_price = float(request.POST.get("product_price"))
        selected.sales_agent = request.POST.get("sales_agent")
        selected.total_amount = float(request.POST.get("total_amount"))

        selected.save()
        return redirect("sales_list")
    return render(request, "salesedit.html", {"selected": selected})

def salesdelete(request, id):
    sales = Sales.objects.get(id=id)
    return render(request, "salesdelete.html", {"sales": sales})

def salesview(request, id):
    sale = get_object_or_404(Sales, id=id)
    return render(request, "salesview.html", {"selected_sale": sale})

# the adduser views
def adduser(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        role = request.POST.get("role")
        password = request.POST.get("password")

        user = Add_user(name=name, email=email,role=role, password=password)
        user.save()
        return redirect("user_list")  # Redirect to a user list or success page
    return render(request, "add_user.html")

def user_list(request):
    users = Add_user.objects.all()
    return render(request, "user_list.html", {"users": users})

def user_edit(request, id):
    selected = Add_user.objects.get(id=id)

    if request.method == "POST":
        selected.name = request.POST.get("name")
        selected.email = request.POST.get("email")
        selected.role = request.POST.get("role")
        selected.password = request.POST.get("password")
        selected.save()
        return redirect("user_list")  # or wherever you want to go after editing

    return render(request, "user_edit.html", {"selected": selected})

def user_delete(request, id):
    selected = Add_user.objects.get(id=id)
    return render(request, "user_delete.html", {"selected": selected})

def user_view(request, id):
    selected = get_object_or_404(Add_user, id=id)
    return render(request, "user_view.html", {"selected": selected})

def logout(request):
    return render(request, "logout.html")