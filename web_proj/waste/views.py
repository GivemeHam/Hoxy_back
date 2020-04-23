from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import waste_type

def home(request):
    return HttpResponse("Hello, Django!")

def select_waste_type(request):
    #results = waste_type.objects.all()
    result = waste_type.objects.filter(waste_type(waste_type_name='cjdthrl'))
    rst = waste_type.objects.order_by('waste_type_no')[0:5]
    
    list = []
    for rst in results:
        dic = {}
        dic['waste_type_no'] = rst.waste_type_no
        dic['waste_type_waste_div_no'] = rst.waste_type_waste_div_no
        dic['waste_type_name'] = rst.waste_type_name
        dic['waste_type_kor_name'] = rst.waste_type_kor_name
        dic['waste_type_size'] = rst.waste_type_size
        dic['waste_type_fee'] = rst.waste_type_fee
        dic['waste_type_area_no'] = rst.waste_type_area_no
        list.append(dic)
        
    context = {'result_value':list}
    return render(request, 'waste_db/waste_type.html', context )