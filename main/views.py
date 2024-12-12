from django.shortcuts import render
from django.http.response import HttpResponse
from database import get_db
from . import func
from . import queries

# Create your views here.
def home(request):
    return render(request,'index.html')

def type(request):
    params = ['2024-12-01','2024-12-31']
    types = [{
        "id":i[0],
        "type_name":i[1],
        "quantity":i[2],
        "sum":i[3],
        }for i in func.get_data(query=queries.types,db=get_db(dbname='o'),params=params)]
    print(types)
    context = {
        'types': types,
    }
    return render(request, 'types.html', context)