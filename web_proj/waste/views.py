from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import waste_type
from .models import waste_div
from .models import user_info
from .models import board_review
from .models import board
from .models import area
from .models import apply_info
from ast import literal_eval

def home(request):
    return HttpResponse("Hello, Django!")

#request_data
#waste_type_name, waste_type_area_no
#response_data
#waste_type
def select_waste_type(request):
   # results = waste_type.objects.all()
    data = request.GET.get("data")
    data_dic = literal_eval(data)
    results = waste_type.objects.filter(waste_type_name=data_dic['waste_type_name'], waste_type_area_no=data_dic['waste_type_area_no'])
    
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

#request_data
#waste_type_name, waste_type_area_no

def insert_waste_apply_info(request):
    data = request.GET.get("data")
    data_dic = literal_eval(data)

    #insert
    result = apply_info(apply_info_name=data_dic['apply_info_name'],
                        apply_info_address=data_dic['apply_info_address'],
                        apply_info_phone=data_dic['apply_info_phone'],
                        apply_info_waste_type_no=data_dic['apply_info_waste_type_no'],
                        apply_info_fee=data_dic['apply_info_fee'],
                        apply_info_code=data_dic['apply_info_code'],
                        apply_info_user_no=data_dic['apply_info_user_no'], )
    result.save()

    context = {'result_value':"success"}
    return render(request, 'waste_db/apply_info.html', context )
