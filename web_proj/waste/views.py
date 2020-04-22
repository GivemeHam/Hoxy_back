from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import waste_type

def home(request):
    return HttpResponse("Hello, Django!")

def select_waste_type(request):
    results = waste_type.objects.all()
    rst = waste_type.objects.order_by('waste_type_no')[0:5]
    str = ''
    for rst in results:
        str += "{}{}{}{}{}{}{}".format(rst.waste_type_no, rst.waste_type_waste_div_no, rst.waste_type_name, rst.waste_type_kor_name, rst.waste_type_size, rst.waste_type_fee, rst.waste_type_area_no)
        

    #result = waste_type.objects.filter(waste_type(waste_type_name='cjdthrl') & waste_type(waste_type_area=1))
    context = {'result_value':str}
    return render(request, 'waste_db/waste_type.html', context )