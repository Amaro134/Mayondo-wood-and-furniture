from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal, InvalidOperation
from datetime import datetime

from .models import Stock, Sales, Add_user
from .forms import Add_userForm, SalesForm, StockForm, Add_userAuthenticationForm

# NOTE: Landing and login pages moved to authentication app

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


@login_required
def addStock(request):
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        type_of_product = request.POST.get("type_of_product")
        costprice = request.POST.get("costprice")
        selling_price = request.POST.get("selling_price")
        quantity = request.POST.get("quantity")
        supplier_name = request.POST.get("supplier_name")
        date_added = request.POST.get("date_added")
        quality = request.POST.get("quality")

        errors = []

        # Validate empty fields
        if not all([product_name, type_of_product, costprice, selling_price, quantity, supplier_name, date_added, quality]):
            errors.append("All fields are required.")

        # Validate number fields
        try:
            costprice = float(costprice)
            selling_price = float(selling_price)
            quantity = int(quantity)
        except ValueError:
            errors.append("Please enter valid numbers for cost, price, and quantity.")

        # Validate positive numbers
        if not errors and (costprice <= 0 or selling_price <= 0 or quantity <= 0):
            errors.append("Values must be greater than zero.")

        # Validate date format
        try:
            datetime.strptime(date_added, "%Y-%m-%d")
        except ValueError:
            errors.append("Invalid date format.")

        if errors:
            return render(request, "stock.html", {
                "errors": errors,
                "product_name": product_name,
                "type_of_product": type_of_product,
                "costprice": costprice,
                "selling_price": selling_price,
                "quantity": quantity,
                "supplier_name": supplier_name,
                "date_added": date_added,
                "quality": quality
            })

        # Save stock
        stock = Stock(
            product_name=product_name,
            type_of_product=type_of_product,
            costprice=costprice,
            selling_price=selling_price,
            quantity=quantity,
            supplier_name=supplier_name,
            date_added=date_added,
            quality=quality
        )
        stock.save()
        messages.success(request, "Stock added successfully!")
        return redirect("stock_list")

    return render(request, "stock.html")


@login_required
def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, "stocklist.html", {"stocks": stocks})

# ---------------- Edit Stock ----------------
@login_required
def stockedit(request, id):
    stock = get_object_or_404(Stock, pk=id)

    if request.method == 'POST':
        stock.product_name = request.POST.get('product_name')
        stock.type_of_product = request.POST.get('type_of_product')
        stock.costprice = request.POST.get('cost_price')  #  matches model field
        stock.sellingprice = request.POST.get('selling_price')
        stock.quantity = request.POST.get('quantity')
        stock.suppliername = request.POST.get('supplier_name')
        stock.date_added = request.POST.get('date_added')
        stock.quality = request.POST.get('quality')
        stock.color = request.POST.get('color')
        stock.measurements = request.POST.get('measurements')

        # Ensure costprice is not None or empty
        if not stock.costprice:
            stock.costprice = 0  # or some default value

        stock.save()
        return redirect('stock_list')  # redirect to your stock list page

    return render(request, 'stockedit.html', {'selected': stock})


# View one stock item by ID
@login_required
def stockview(request, id):
    stock = get_object_or_404(Stock, id=id)
    return render(request, "stockview.html", {"selected": stock})

@login_required
def stockdelete(request, id):
    stock = get_object_or_404(Stock, id=id)
    if request.method == "POST":
        stock.delete()
        return redirect('stock_list')
    return render(request, "stockdelete.html", {"stock": stock})
 # make sure this matches your URL name

@login_required
def stockupdate(request, id):
    stock = get_object_or_404(Stock, id=id)
    # Example: maybe you want to show a prefilled form
    return render(request, "stockedit.html", {"stock": stock})

# ---------------- Dashboard ----------------
@login_required
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


# views.py
from decimal import Decimal

@login_required
def add_sales(request):
    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        product = request.POST.get("product")
        quantity_sold = request.POST.get("quantity_sold")
        product_price = request.POST.get("product_price")
        total_amount = request.POST.get("total_amount")
        payment_method = request.POST.get("payment_method")
        transport_used = request.POST.get("transport_used")
        date_of_sale = request.POST.get("date_of_sale")
        sales_agent = request.POST.get("sales_agent")

        # Check required fields
        if not all([customer_name, product, quantity_sold, product_price, payment_method, transport_used, date_of_sale, sales_agent]):
            messages.error(request, "Please fill in all required fields.")
            return redirect("add_sales")

        # Validate numeric fields
        try:
            quantity_sold = Decimal(quantity_sold)
            product_price = Decimal(product_price)
        except InvalidOperation:
            messages.error(request, "Quantity and Product Price must be valid numbers.")
            return redirect("add_sales")

        if quantity_sold <= 0 or product_price <= 0:
            messages.error(request, "Quantity and Product Price must be greater than zero.")
            return redirect("add_sales")

        # Calculate total if not entered
        if not total_amount:
            total_amount = quantity_sold * product_price
        else:
            try:
                total_amount = Decimal(total_amount)
            except InvalidOperation:
                messages.error(request, "Total amount must be a valid number.")
                return redirect("add_sales")

        # Save the sale
        sale = Sales(
            customer_name=customer_name,
            product=product,
            quantity_sold=quantity_sold,
            product_price=product_price,
            total_amount=total_amount,
            payment_method=payment_method,
            transport_used=transport_used,
            date_of_sale=date_of_sale,
            sales_agent=sales_agent,
        )
        sale.save()
        messages.success(request, "Sale added successfully!")
        return redirect("sales_list")

    return render(request, "add_sales.html")
# List all sales
@login_required
def sales_list(request):
    all_sales = Sales.objects.all()
    return render(request, "sales_list.html", {"sales": all_sales})

@login_required
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

@login_required
def salesdelete(request, id):
    sales = get_object_or_404(Sales, id=id)
    
    if request.method == "POST":
        sales.delete()  # actually deletes the record
        return redirect("sales_list")  # redirect to your sales list view
    
    # if GET, show confirmation page
    return render(request, "salesdelete.html", {"sales": sales})

@login_required
def salesview(request, id):
    sale = get_object_or_404(Sales, id=id)
    return render(request, "salesview.html", {"selected_sale": sale})
#---- receipt-----
@login_required
def salesreceipt(request, sale_id):
    sale = get_object_or_404(Sales, id=sale_id)
    return render(request, 'salesreceipt.html', {'sale': sale})

# the adduser views
@login_required
def adduser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        role = request.POST.get("role")
        password = request.POST.get("password")

        #  Validation checks
        if not username or not email or not role or not password:
            messages.error(request, "All fields are required.")
            return render(request, "add_user.html")

        if Add_user.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "add_user.html")

        if Add_user.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "add_user.html")

        #  Create user
        user = Add_user(username=username, email=email, role=role)
        user.set_password(password)  # hash password properly
        user.save()

        messages.success(request, "User added successfully!")
        return redirect("user_list")  # redirect to user list page

    return render(request, "add_user.html")

@login_required
def user_list(request):
    users = Add_user.objects.all()
    return render(request, "user_list.html", {"users": users})

@login_required
def user_edit(request, id):
    selected = Add_user.objects.get(id=id)

    if request.method == "POST":
        selected.name = request.POST.get("username")
        selected.email = request.POST.get("email")
        selected.role = request.POST.get("role")
        selected.password = request.POST.get("password")
        selected.save()
        return redirect("user_list")  # or wherever you want to go after editing

    return render(request, "user_edit.html", {"selected": selected})

@login_required
def user_delete(request, id):
    selected = Add_user.objects.get(id=id)
    return render(request, "user_delete.html", {"selected": selected})

@login_required
def user_view(request, id):
    selected = get_object_or_404(Add_user, id=id)
    return render(request, "user_view.html", {"selected": selected})

@login_required
def logout(request):
    if request.method == "POST":
        auth_logout(request)  # Logs the user out
        return redirect("/")  # Redirect to homepage after logout
    return render(request, "logout.html")  # Redirect to homepage or login


from django.db.models import Sum

# Report dashboard – overview page
@login_required
def report_dashboard(request):
    total_sales = Sales.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    total_stock = Stock.objects.count()
    total_products = Stock.objects.values('product_name').distinct().count()
    return render(request, "report.html", {
        "total_sales": total_sales,
        "total_stock": total_stock,
        "total_products": total_products,
    })

# Sales report – detailed sales data
@login_required
def sales_report(request):
    sales = Sales.objects.all().order_by('-date_of_sale')
    total_sales = sales.aggregate(total=Sum('total_amount'))['total'] or 0
    return render(request, "salesreport.html", {
        "sales": sales,
        "total_sales": total_sales,
    })

# Stock report – all stock items and totals
@login_required
def stock_report(request):
    stocks = Stock.objects.all().order_by('-date_added')
    total_stock = stocks.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    return render(request, "stockreport.html", {
        "stocks": stocks,
        "total_stock": total_stock,
    })

#Combined summary report – sales + stock overview
@login_required
def summary_report(request):
    # --- Sales Summary ---
    total_sales_amount = Sales.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_quantity_sold = Sales.objects.aggregate(Sum('quantity_sold'))['quantity_sold__sum'] or 0
    total_sales_count = Sales.objects.count()

    # --- Stock Summary ---
    total_stock_items = Stock.objects.count()
    total_stock_quantity = Stock.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_stock_value = Stock.objects.aggregate(Sum('costprice'))['costprice__sum'] or 0

    # --- Combined Report Context ---
    context = {
        "total_sales_amount": total_sales_amount,
        "total_quantity_sold": total_quantity_sold,
        "total_sales_count": total_sales_count,
        "total_stock_items": total_stock_items,
        "total_stock_quantity": total_stock_quantity,
        "total_stock_value": total_stock_value,
    }

    return render(request, "summary_report.html", context)

