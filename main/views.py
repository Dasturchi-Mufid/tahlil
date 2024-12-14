from django.shortcuts import render
from database import get_db,BRANCHES
from . import func
from . import queries
from datetime import date
import json

branches = json.loads(BRANCHES)

# Create your views here.
def home(request):
    print(f'get: {request.GET}')
    print(f'post: {request.POST}')
    today = date.today()
    start,end = func.get_date(today.strftime('%Y-%m'))
    context = {
        'branches': branches,
        'today': today.strftime('%Y-%m-%d'),
        'start': start.strftime('%Y-%m-%d'),
    }
    return render(request,'index.html',context)

def typee(request):
    print(request.POST)
    if request.session.get('branch'):
        branch = request.session.get('branch')
    if request.POST.get('branch'):
        request.session['branch'] = branch = request.POST.get('branch','o')
    month = date.today().strftime('%Y-%m')
    start,end = func.get_date(month=month)
    if request.POST.get('date'):
        month = request.POST.get('date')
        start,end = func.get_date(month=month)
    params = [start,end]

    types = [{
        "id":i[0],
        "type_name":i[1],
        "quantity":i[2],
        "sum":i[3],
        }for i in func.get_data(query=queries.types,db=get_db(dbname=branch),params=params)]
    types_total = {
        "types":len(types),
        "quantity": sum(i['quantity'] for i in types),
        "sum": sum(i['sum'] for i in types),
    }
    
    for t in types:
        t['percentage'] = round((t['sum'] / types_total['sum']) * 100, 2)
    
    if request.POST.get('branch_excel') and request.POST.get('month'):
        print('excel')
        branch_ = request.POST.get('branch_excel')
        month_ = request.POST.get('month')
        return func.download_type_xlsx(request,month_,branch_,types)

    context = {
        'month':month,
        'types': types,
        'types_total': types_total,
        'branches':branches
    }
    
    return render(request, 'types.html', context)

def type_detail(request,id):
    request.session['branch'] = branch = request.session.get('branch','o')
    month = date.today().strftime('%Y-%m')
    start,end = func.get_date(month=month)
    if request.POST.get('date'):
        month = request.POST.get('date')
        start,end = func.get_date(month=month)
    params = [start, end,id]
    # print(func.get_data(query=queries.product,db=get_db(dbname=branch),params=params))
    products = [{
        "type_id":i[0],
        "type":i[1],
        "product":f'{i[2]} {i[3]} {i[4]}',
        "quantity":i[5],
        "price":i[6],
        "total":i[7],
        "income":i[8].strftime("%d.%m.%Y"),
        "out":i[9].strftime("%d.%m.%Y"),
        "difference":(i[9]-i[8]).days
        } for i in func.get_data(query=queries.product,db=get_db(dbname=branch),params=params)]
    totals = {
        "products":len(products),
        "quantity": sum(i['quantity'] for i in products),
        "total": sum(i['total'] for i in products)
    }
    if request.POST.get('month') and request.POST.get('branch_excel'):
        month_ = request.POST.get('month')
        branch_ = request.POST.get('branch_excel')
        tur = products[0].get('type') if products else ''
        return func.download_type_detail_xlsx(request,month_,branch_,products,tur)
    context = {
        'products': products,
        'branches':branches,
        'month':month,
        'totals': totals
    }
    return render(request,'type_detail.html',context)