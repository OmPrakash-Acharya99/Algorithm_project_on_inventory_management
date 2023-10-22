from django.shortcuts import render,redirect
from django.http  import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product
from .models import Order,File
from django.shortcuts import get_object_or_404
from .forms import ProductForm,OrderForm
from django.contrib.auth.models import User
from django.contrib import messages
import pandas as pd 
from django.http import JsonResponse




@login_required(login_url='user-login')
def index(request):
    orders = Order.objects.all()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
    else:
        form = OrderForm()
    context = {
        'orders': orders,
        'form': form,
    }
    return render(request, 'dashboard/index.html', context)
# Create your views here.



@login_required(login_url = 'user-login')
def staff(request):
   workers = User.objects.all()
   context= {
      'workers' : workers
   }
    
   return render(request,'dashboard/staff.html',context)




@login_required(login_url='user-login')
def staff_detail(request, pk):
    worker = User.objects.get(id=pk)
    context = {
        'worker': worker,
    }
    return render(request, 'dashboard/staff_detail.html', context)



@login_required(login_url='user-login')
def staff_delete(request, pk):
    # Use get_object_or_404 to handle the case where the user does not exist
    worker = get_object_or_404(User, id=pk)

    if request.method == "POST":
        worker.delete()
        return redirect('dashboard-staff')

    return render(request, 'dashboard/staff_delete.html')
      

import pandas as pd

def create_db(file_path):
         df = pd.read_csv(file_path, delimiter = ",")
         print(df)
         list_of_csv = [list(row) for row in df.values]
         for l in list_of_csv:
  
            if len(l) == 3:  # Check if the row has exactly three columns
                product = Product.objects.create(
                    name=l[0],       # Assuming the name is in the first column (index 0)
                    category=l[1],   # Assuming the category is in the second column (index 1)
                    quantity=l[2],   # Assuming the quantity is in the third column (index 2)
                )
                product.save()
     


# Define the products views

from django.db import IntegrityError

@login_required(login_url='user-login') #sorting happens in this functions
def products(request):
    # File Upload Handling
    if request.method == "POST" and 'file' in request.FILES:
        file = request.FILES['file']
        obj = File.objects.create(file=file)
        try:
            create_db(obj.file)
        except IntegrityError as e:
            # Handle the case where duplicate data is found
            messages.error(request, 'Error: Duplicate data found in the CSV file.')
            return redirect('dashboard-products')

        # Redirect or do anything else after processing the file upload
        return redirect('dashboard-products')

    # Form Handling
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                product_name = form.cleaned_data.get('name')
                messages.success(request, f'{product_name} has been added successfully')
                return redirect('dashboard-products')
            except IntegrityError as e:
                # Handle the case where duplicate data is found
                messages.error(request, 'Error: Duplicate data found in the form submission.')
                return redirect('dashboard-products')
    else:
        form = ProductForm()
    # Retrieve and Sort Items
    
    def insertion_sort(items): # when uploading from dtabase 
        items_list = list(items)  # Convert the queryset to a list
        for i in range(1, len(items_list)):
            key = items_list[i]
            j = i - 1
            while j >= 0 and key.name < items_list[j].name:
                items_list[j + 1] = items_list[j]
                j -= 1
            items_list[j + 1] = key
        return items_list
    
    items = Product.objects.all() 
    sorted_items = insertion_sort(items)


    def bubble_sort(items, key, ascending=True):
        n = len(items)
        for i in range(n):
            for j in range(0, n-i-1):
                comparison_result = getattr(items[j], key) > getattr(items[j+1], key)
                if ascending:
                    should_swap = comparison_result
                else:
                    should_swap = not comparison_result

                if should_swap:
                    items[j], items[j+1] = items[j+1], items[j]

    # Sorting Handling using Bubble Sort
    sort_by = request.GET.get('sort_by', 'name')  # Default to sorting by name
    items = list(Product.objects.all())  # Convert the queryset to a list for sorting

    # Determine sorting order (ascending or descending)
    sort_order = request.GET.get('sort_order', 'asc')  # Default to ascending
    ascending = sort_order.lower() == 'asc'

    # Toggle sorting order for the next click
    next_sort_order = 'desc' if sort_order.lower() == 'asc' else 'asc'


    # Sort items based on sort_by key using bubble sort
    if sort_by == 'quantity':
        bubble_sort(items, 'quantity', ascending)
    elif sort_by == 'category':
        bubble_sort(items, 'category', ascending)
    else:
        bubble_sort(items, 'name', ascending)
    context = {
        'items': items,
        'form': form,
        'current_sort': sort_by,
        'next_sort_order':next_sort_order, 
    }


    return render(request, 'dashboard/products.html', context)




@login_required(login_url='user-login')
def product_delete(request,pk):
       item = Product.objects.get(id=pk)
       if request.method == "POST":
              item.delete()
              return redirect('dashboard-products')
       
       return render(request,'dashboard/product_delete.html')

@login_required(login_url='user-login')
def product_update(request,pk):
       item = Product.objects.get(id=pk)
       if request.method == "POST":
            form = ProductForm(request.POST,instance= item)
            if form.is_valid():
                   form.save()
                   return redirect('dashboard-products')
       else:
           form = ProductForm(instance=item)       
       context = {
           'form': form
       }
       return render(request , "dashboard/product_update.html",context)
       
       
       
@login_required(login_url = 'user-login')
def order(request):
    orders = Order.objects.all()
    context = {
        'orders': orders
    }
    return render(request,'dashboard/order.html',context)


from django.views.decorators.csrf import csrf_exempt

from django.db.models import F


@csrf_exempt
def export_data_to_excel(request):
    if request.method == 'POST':
        orders = Order.objects.all()

        # Convert the queryset to a list of dictionaries
        data = list(orders.values(
            'product__name',
            'product__category',
            'product__quantity',
            'staff__username',
            'order_quantity',
            'date',  # Use the original 'date' field here
        ))

        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(data)

        # Check if the 'date' field is present in the DataFrame and if it is a 'datetime' object
        if 'date' in df.columns and df['date'].dtype != object:
            # Convert the 'date' field to timezone-unaware
            df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)
        else:
            # Handle the case where 'date' is not present in the DataFrame or it is not a 'datetime' object
            raise KeyError("The 'date' field is not present in the DataFrame or it is not a 'datetime' object.")

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=output.xlsx'
        df.to_excel(response, index=False)

        return response

    # If it's a GET request, render the template
    orders = Order.objects.all()  # You might want to pass the data to the template
    return render(request, 'dashboard/order.html', {'orders': orders})





@csrf_exempt
def export_data_to_excel_from_product(request):
    if request.method == 'POST':
        products = Product.objects.all()

        # Convert the queryset to a list of dictionaries
        data = list(products.values(
            'name',
            'category',
            'quantity',
            # Remove 'date' from here since it's not a field in Product model
        ))

        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(data)

        # Convert the 'date' field to timezone-unaware if it exists
        # Note: This part can be omitted if 'date' is not in the queryset
        if 'date' in df.columns:
            df['date'] = df['date'].apply(lambda x: x.replace(tzinfo=None) if x is not None else x)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=output.xlsx'
        df.to_excel(response, index=False)

        return response

    # If it's a GET request, render the template
    products = Product.objects.all()  # You might want to pass the data to the template
    return render(request, 'dashboard/products.html', {'products': products})





  
@login_required(login_url='user-login')
def order_update(request, pk):
    order = Order.objects.get(id=pk)  # Use get_object_or_404 to handle the case where the order does not exist
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard-index')  # Fix typo: 'dashboard-staff_index'
    else:
        form = OrderForm(instance=order)

    context = {
        'form': form,
    }

    return render(request, "dashboard/order_update.html", context)


@login_required(login_url='user-login')
def order_delete(request, pk):
       order = Order.objects.get(id=pk)
       if request.method == "POST":
              order.delete()
              return redirect('dashboard-index')
       
       return render(request,'dashboard/order_delete.html')


@login_required(login_url='user-login')
def order_cancel(request, pk):
       order = Order.objects.get(id=pk)
       if request.method == "POST":
              order.delete()
              return redirect('dashboard-order')
       
       return render(request,'dashboard/order_cancel.html')
   
  
