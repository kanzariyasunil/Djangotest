from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Orders,OrdersUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt 
def index(request):
    # products = Product.objects.all()
    # n = len(products) 
    # nslides = n//4 + ceil((n/4) - (n//4))
    # params = {'no_of_slides':nslides,"range":range(1,nslides+1),"product":products}
    # allprods = [[products,range(1,nslides),nslides],[products,range(1,nslides),nslides]]
    
    
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {"allProds":allProds}
    return render(request,'index2.html',params)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'search.html', params)

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        Email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contact = Contact(name = name, Email =Email,phone = phone,desc = desc)
        contact.save()
        name = contact.name
        return render(request,'contact.html',{'name':name})
    
    return render(request,'contact.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrdersUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success","updates":updates,"itemsJson":order[0].item_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'tracker.html')




def prodView(request,myid):
    product = Product.objects.filter(id = myid)
    return render(request,'prodView.html',{'product':product[0]})

def checkout(request):
    if request.method == 'POST':
        item_json = request.POST.get('itemJson','')
        amount = request.POST.get('amount','')
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        address = request.POST.get('address1','') + " " + request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        orders = Orders(item_json = item_json,name = name, email =email,phone = phone,address = address,city = city,state =state,
                          zip_code =zip_code,amount = amount)
        orders.save()
        update = OrdersUpdate(order_id = orders.order_id,update_desc = "The order has been placed")
        update.save()
        thank = True
        id = orders.order_id
        # return render(request,'checkout.html',{'thank' :thank,'id':id})
           # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        #request paytm to transfer the amount to your account after payment by user
        param_dict={

            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(orders.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

                    }
        
        return  render(request, 'paytm.html', {'param_dict': param_dict})

        
    return render(request,'checkout.html')


@csrf_exempt
def handlerequest(request):
    amount = request.POST.get('amount','')
    return render(request,'paymentstatus.html',{'amount':amount})