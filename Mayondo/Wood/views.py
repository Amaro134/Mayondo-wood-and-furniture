from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Stock, Sales, Add_user
from datetime import datetime
from .forms import Add_userForm, SalesForm, StockForm, Add_userAuthenticationForm
from decimal import Decimal, InvalidOperation
from django.contrib.auth import logout as auth_logout, authenticate, login as auth_login
from django.contrib import messages
#from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.db.models import Sum, Avg, Count



# ---------------- Landing ----------------
def landingPage(request):
    return render(request, "index.html")

def login_view(request):
    print("login view called")
    if request.method == "POST":
        form = Add_userAuthenticationForm(request.POST)
        if form.is_valid():  # fixed typo here
            print("login is valid")
            user = form.cleaned_data.get('user')
            auth_login(request, user)
            return redirect("dashboard")
        else:
            print("login form has errors")
            print(form.errors)
    else:
            print("something wrong")
            form = Add_userAuthenticationForm()
    return render(request, "login.html", {"form": form})

            

# ---------------- Dashboard ----------------

@login_required
def dashboard(request):
    user = request.user

    # Determine user role (ensure it’s stored on your custom user model)
    user_role = getattr(user, "role", None)

    # Sales data
    if user.is_superuser or user_role in ["Admin", "Manager"]:
        sales = Sales.objects.all().order_by('-date_of_sale')[:5]
        show_stock = True  # Admins/Managers see stock cards & table
    elif user_role == "Sales Agent":
        sales = Sales.objects.filter(sales_agent=user).order_by('-date_of_sale')[:5]
        show_stock = False  # Hide stock cards & table for sales agents
    else:
        return HttpResponseForbidden("You do not have access to this dashboard.")

    total_stock = Stock.objects.count() if show_stock else None
    current_stock = Stock.objects.aggregate(Sum('quantity'))['quantity__sum'] if show_stock else None
    restock_value = Stock.objects.aggregate(Sum('selling_price'))['selling_price__sum'] if show_stock else None

    context = {
        "sales": sales,
        "show_stock": show_stock,
        "total_stock": total_stock,
        "current_stock": current_stock,
        "restock_value": restock_value,
        "stocks": Stock.objects.all().order_by('-date_added')[:5] if show_stock else None,
        "user_role": user_role,  #  Add this line
    }

    return render(request, "dashboard.html", context)


# ---------------- Stock Views ----------------
@login_required
def addStock(request):
    if request.user.role not in ["Admin", "Manager"]:
        return HttpResponseForbidden("You are not authorized to access this page.")
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

        if not all([product_name, type_of_product, costprice, selling_price, quantity, supplier_name, date_added, quality]):
            errors.append("All fields are required.")

        try:
            costprice = float(costprice)
            selling_price = float(selling_price)
            quantity = int(quantity)
        except ValueError:
            errors.append("Please enter valid numbers for cost, price, and quantity.")

        if not errors and (costprice <= 0 or selling_price <= 0 or quantity <= 0):
            errors.append("Values must be greater than zero.")

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
#----stock_list----------
@login_required
def stock_list(request):
    if request.user.role not in ["Admin", "Manager"]:
        return HttpResponseForbidden("You are not authorized to access this page.")
    stocks = Stock.objects.all()
    return render(request, "stocklist.html", {"stocks": stocks})




@login_required
def stockedit(request, id):
    if request.user.role not in ["Admin", "Manager"]:
        return HttpResponseForbidden("You are not authorized to access this page.")
    stock = get_object_or_404(Stock, pk=id)

    if request.method == 'POST':
        stock.product_name = request.POST.get('product_name')
        stock.type_of_product = request.POST.get('type_of_product')
        stock.costprice = request.POST.get('costprice')
        stock.selling_price = request.POST.get('selling_price')
        stock.quantity = request.POST.get('quantity')
        stock.supplier_name = request.POST.get('supplier_name')
        stock.date_added = request.POST.get('date_added')
        stock.quality = request.POST.get('quality')
        stock.color = request.POST.get('color')
        stock.measurements = request.POST.get('measurements')

        if not stock.costprice:
            stock.costprice = 0

        stock.save()
        return redirect('stock_list')

    return render(request, 'stockedit.html', {'selected': stock})

@login_required
def stockview(request, id):
    if request.user.role not in ["Admin", "Manager"]:
        return HttpResponseForbidden("You are not authorized to access this page.")
    stock = get_object_or_404(Stock, id=id)
    return render(request, "stockview.html", {"selected": stock})

@login_required
def stockdelete(request, id):
    if request.user.role not in ["Admin", "Manager"]:
        return HttpResponseForbidden("You are not authorized to access this page.")
    stock = get_object_or_404(Stock, id=id)
    if request.method == "POST":
        stock.delete()
        return redirect('stock_list')
    return render(request, "stockdelete.html", {"stock": stock})

@login_required
def stockupdate(request, id):
    if request.user.role not in ["Admin", "Manager"]:
        return HttpResponseForbidden("You are not authorized to access this page.")
    stock = get_object_or_404(Stock, id=id)
    return render(request, "stockedit.html", {"stock": stock})




# ---------------- Sales Views ----------------
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

        if not all([customer_name, product, quantity_sold, product_price, payment_method, transport_used, date_of_sale, sales_agent]):
            messages.error(request, "Please fill in all required fields.")
            return redirect("add_sales")

        try:
            quantity_sold = Decimal(quantity_sold)
            product_price = Decimal(product_price)
        except InvalidOperation:
            messages.error(request, "Quantity and Product Price must be valid numbers.")
            return redirect("add_sales")

        if quantity_sold <= 0 or product_price <= 0:
            messages.error(request, "Quantity and Product Price must be greater than zero.")
            return redirect("add_sales")

        if not total_amount:
            total_amount = quantity_sold * product_price
        else:
            try:
                total_amount = Decimal(total_amount)
            except InvalidOperation:
                messages.error(request, "Total amount must be a valid number.")
                return redirect("add_sales")

        if transport_used.replace("_", " ").lower() == "company provision":
            extra_charge = total_amount * Decimal("0.05")
            total_amount += extra_charge

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



def stock_report(request):
    stocks = Stock.objects.all().order_by('-date_added')

    # Date filter
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        stocks = stocks.filter(date_added__range=[start_date, end_date])

    total_products = stocks.count()
    total_quantity = stocks.aggregate(total=Sum('quantity'))['total'] or 0
    total_value = stocks.aggregate(total=Sum('selling_price'))['total'] or 0
    low_stock_count = stocks.filter(quantity__lt=5).count()

    context = {
        'stocks': stocks,
        'total_products': total_products,
        'total_quantity': total_quantity,
        'total_value': total_value,
        'low_stock_count': low_stock_count,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, "stockreport.html", context)

# -----Sales_list view-----------
@login_required
def sales_list(request):
    user = request.user

    if user.is_superuser or user.role in ["Admin", "Manager"]:
        sales = Sales.objects.all().order_by('-date_of_sale')
    elif user.role == "Sales Agent":
        sales = Sales.objects.filter(sales_agent=user).order_by('-date_of_sale')
    else:
        return HttpResponseForbidden("You do not have access to this page.")

    context = {"sales": sales}
    return render(request, "sales_list.html", context)

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
    sales = get_object_or_404(Sales, id=id)
    if request.method == "POST":
        sales.delete()
        return redirect("sales_list")
    return render(request, "salesdelete.html", {"sales": sales})


def salesview(request, id):
    sale = get_object_or_404(Sales, id=id)
    return render(request, "salesview.html", {"selected_sale": sale})


def salesreceipt(request, sale_id):
    sale = get_object_or_404(Sales, id=sale_id)
    return render(request, 'salesreceipt.html', {'sale': sale})


# ---------------- User Views ----------------
def adduser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        role = request.POST.get("role")
        password = request.POST.get("password")
        

        if not username or not email or not role or not password:
            messages.error(request, "All fields are required.")
            return render(request, "add_user.html")

        if Add_user.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "add_user.html")

        if Add_user.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "add_user.html")
        
        print(password)
        user = Add_user(username=username, email=email, role=role)
        user.set_password(password)
        user.save()

        messages.success(request, "User added successfully!")
        return redirect("user_list")

    return render(request, "add_user.html")


def user_list(request):
    users = Add_user.objects.all()
    return render(request, "user_list.html", {"users": users})


def user_edit(request, id):
    selected = get_object_or_404(Add_user, id=id)

    if request.method == 'POST':
        form = Add_userForm(request.POST, instance=selected)
        if form.is_valid():
            user = form.save(commit=False)

            # Preserve old password if no new one provided
            if not form.cleaned_data.get('password'):
                user.password = selected.password
            else:
                user.set_password(form.cleaned_data['password'])

            user.save()
            return redirect('user_list')
    else:
        form = Add_userForm(instance=selected)

    # Notice we’re passing BOTH `form` and `selected` to the template
    return render(request, 'user_edit.html', {
        'form': form,
        'selected': selected,
    })

def user_delete(request, id):
    selected = Add_user.objects.get(id=id)
    return render(request, "user_delete.html", {"selected": selected})


def user_view(request, id):
    selected = get_object_or_404(Add_user, id=id)
    return render(request, "user_view.html", {"selected": selected})


def logout_view(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect("login")
    return render(request, "logout.html")


# ---------------- Reports ----------------
def report_dashboard(request):
    total_sales = Sales.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    total_stock = Stock.objects.count()
    total_products = Stock.objects.values('product_name').distinct().count()
    return render(request, "report.html", {
        "total_sales": total_sales,
        "total_stock": total_stock,
        "total_products": total_products,
    })



@login_required
def sales_report(request):
    sales = Sales.objects.all().order_by('-date_of_sale')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        sales = sales.filter(date_of_sale__range=[start_date, end_date])

    # Summary values
    total_sales_count = sales.count()
    total_revenue = sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    avg_sale = sales.aggregate(Avg('total_amount'))['total_amount__avg'] or 0

    # Find top product
    top = (
        sales.values('product')
        .annotate(total_sold=Sum('quantity_sold'))
        .order_by('-total_sold')
        .first()
    )
    top_product = top['product'] if top else None

    context = {
        'sales': sales,
        'total_sales_count': total_sales_count,
        'total_revenue': total_revenue,
        'avg_sale': round(avg_sale, 2),
        'top_product': top_product,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, "salesreport.html", context)
