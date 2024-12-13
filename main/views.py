from django.shortcuts import render
from database import get_db,BRANCHES
from . import func
from . import queries
from datetime import date
import json

branches = json.loads(BRANCHES)

# Create your views here.
def home(request):
    return render(request,'index.html')

def type(request):
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
    
    context = {
        'month':month,
        'types': types,
        'types_total': types_total,
        'branches':branches
    }
    
    return render(request, 'types.html', context)

def type_detail(request,id):
    print(request.POST)
    request.session['branch'] = branch = request.session.get('branch','o')
    print(request.session['branch'])
    print(f'branch: {branch}')
    month = date.today().strftime('%Y-%m')
    start,end = func.get_date(month=month)
    if request.POST.get('date'):
        month = request.POST.get('date')
        start,end = func.get_date(month=month)
    params = [start, end,id]
    products = [{
        "type_id":i[0],
        "type":i[1],
        "product":f'{i[2]} {i[3]} {i[4]}',
        "quantity":i[5],
        "price":i[6],
        "total":i[7],
        "income":i[8],
        "out":i[9],
        "difference":(i[9]-i[8]).days
        } for i in func.get_data(query=queries.product,db=get_db(dbname=branch),params=params)]
    context = {
        'products': products,
        'branches':branches,
        'month':month
    }
    return render(request,'type_detail.html',context)