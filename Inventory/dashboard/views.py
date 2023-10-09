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
def staff_delete(request,pk):
       worker =User.objects.get(id=pk)
       if request.method == "POST":
              worker.delete()
              return redirect('dashboard-staff')
       
       return render(request,'dashboard/staff_delete.html')
      



def insertion_sort(items):
    for i in range(1, len(items)):
        key = items[i]
        j = i - 1
        while j >= 0 and key.name < items[j].name:
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = key


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
     
     
# Define the products view
@login_required(login_url='user-login') # we have also used ORM ( Object Relational Mapping )
def products(request):
    if request.method  == "POST":
      if 'file' in request.FILES:  
        file = request.FILES['file']
        obj=File.objects.create(file=file)
        create_db(obj.file)
    items = list(Product.objects.all())  # Retrieve all items from the database and convert to a list
    insertion_sort(items)  # Manually sort items using insertion sort
    if request.method == "POST":
           form = ProductForm(request.POST)
           if form.is_valid():
                  form.save()
                  product_name = form.cleaned_data.get('name')
                  messages.success(request,f'{product_name} has been added successfully')
                  return redirect('dashboard-products')
                  
    else: 
        form = ProductForm()    
    context = {
        'items': items,
        'form' : form,
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


@csrf_exempt
def export_data_to_excel(request):
    if request.method == 'POST':
        orders = Order.objects.all()

        # Get related product information
        orders = orders.select_related('product', 'staff')

        # Convert the queryset to a list of dictionaries
        data = list(orders.values(
            'product__name',
            'product__category',
            'product__quantity',
            'staff__username',
            'order_quantity',
            'date',
        ))

        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(data)

        # Convert the 'date' field to timezone-unaware
        df['date'] = df['date'].apply(lambda x: x.replace(tzinfo=None) if x is not None else x)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=output.xlsx'
        df.to_excel(response, index=False)

        return response

    # If it's a GET request, render the template
    orders = Order.objects.all()  # You might want to pass the data to the template
    return render(request, 'dashboard/order.html', {'orders': orders})

  
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
   
   
def approve_orders_and_notify(request,pk):
    if request.method == 'POST':
      
            order.is_approved = True
            order.save()

            # Send notification to the staff user
            staff = order.staff         
            messages.success(request, f'Order approved. Notification sent to {staff.username}')

            return redirect('dashboard-order')


    return render(request,'dashboard/order_approve.html')
  