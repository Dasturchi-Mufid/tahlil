from django.shortcuts import render
from database import get_db,BRANCHES
from . import func
from . import queries
from datetime import date
import json
from django.views.decorators.csrf import csrf_exempt


branches = json.loads(BRANCHES)

# Create your views here.
@csrf_exempt
def home(request):
    if not request.session.get('branch'):
        request.session['branch'] = 'o'
    
    branch = request.session.get('branch')
    product_types = [{
        "id":i[0],
        "type_name":i[1]
        } for i in func.get_data(query=queries.product_types, db=get_db(dbname=branch))
    ]
    today = date.today()
    start,end = func.get_date(today.strftime('%Y-%m'))
    end = date.today()

    if request.POST.get('start_date') and request.POST.get('end_date') and (request.session.get('branch') or request.POST.get('branch')):
        result = {}
        branch = request.session.get('branch')
        start,end = func.get_date_range(request.POST.get('start_date'),request.POST.get('end_date'))
        month_dict = func.get_month_ranges(start,end)
        
        for month,date_range in month_dict.items():
            typees = [{
                "id":i[0],
                "type_name":i[1],
                "quantity":i[2],
                "sum":i[3],
                }for i in func.get_data(query=queries.types,db=get_db(dbname=branch),params=date_range)]
            summa = sum(i['sum'] for i in typees)
            for t in typees:
                t['percentage'] = round((t['sum'] / summa) * 100, 2)
            result[month] = typees
        with open('result.json', 'w',) as file:
            json.dump(result, file, default=func.decimal_to_float,indent=4)
    else:
        result = {}
    if request.POST.get('excel_report'):
        return func.download_report_xlsx(request=request,month=[start,end],branch=branch,data=result,product_types=product_types)

    context = {
        'branches': branches,
        'branch':branches.get(request.session.get('branch')),
        'end': end.strftime('%Y-%m'),
        'start': start.strftime('%Y-%m'),
        'result':result
    }
    return render(request,'index.html',context)

@csrf_exempt
def typee(request):
    branch = request.session.get('branch','o')
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

@csrf_exempt
def type_detail(request,id):
    request.session['branch'] = branch = request.session.get('branch','o')
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




def flush(request):
    request.session.flush()