from django.shortcuts import render

from django.http import HttpResponse
from rest_framework.decorators import api_view
import logging
logger = logging.getLogger('test')
#deeplearning
from .deep_learning.inceptionv3_inference import * 
from .forms import *
import os
#models
from .models import *
from ast import literal_eval
from datetime import datetime
#image decode
import base64
from django.core.files.base import ContentFile
#################
# views.py
import requests
from django.http import HttpResponse as Response
import json

tid=0
@api_view(['POST'])
def KakaoPay(request):
    url = "https://kapi.kakao.com/v1/payment/ready"

    payload = "cid=TC0ONETIME&partner_order_id=1001&partner_user_id=gorany&item_name=test&quantity=1&total_amount=777&tax_free_amount=0&approval_url=http://192.168.0.107:8000/KakaoPaySuccess/?random=44&cancel_url=http://192.168.0.107:8000/KakaoPayCancel/&fail_url=http://192.168.0.107:8000/KakaoPayFail/"
    headers = {'Authorization': 'KakaoAK 07bd56b63267b53895005b8792088d79','Content-Type': 'application/x-www-form-urlencoded','Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, headers=headers, data = payload)

    #print(response.text.encode('utf8'),"here------------------------------")
    json_string=response.text.encode('utf8')
    str_json=json_string.decode('utf-8')
    dict_json=json.loads(str_json)
    tid=dict_json['tid']
    #인증 쌍 만들기
    random=44
    result=forpay(random_no=random,
                        tid=tid)
    result.save()
    #
    request.session['tid']=tid
    print(tid,"33333333333333",request.session.get('tid'))
        # context = {'result_value':response}
    # return render(request, 'waste_db/pay.html', context )

    return Response(response)    

#######################
@api_view(['GET'])
def KakaoPaySuccess(request):
    print(request.GET.get("pg_token"),"============here=========================")
    print(request.GET.get("random"),"please!!!!!!!!")
    pg_token=request.GET.get("pg_token")
    #db에서 가져옴
    results=forpay.objects.filter(random_no=44)
    list=[]
    for rst in results :
        dic={}
        dic["random_no"]=rst.random_no
        dic['tid']=rst.tid
        list.append(dic)
    print(list,"wpqkfwpqkfwpqkf0000000")
    tid_no=list[0]['tid']
    #
    print(type(pg_token),"12341234123412341234","tid!!!!",request.session.get('tid'),tid_no)
    #
    url = "https://kapi.kakao.com/v1/payment/approve"

    payload = "cid=TC0ONETIME&partner_order_id=1001&partner_user_id=gorany&tid="+str(tid_no)+"&pg_token="+request.GET.get("pg_token")
    headers = {'Authorization': 'KakaoAK 07bd56b63267b53895005b8792088d79','Content-Type': 'application/x-www-form-urlencoded','Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, headers=headers, data = payload)

    print(response.text.encode('utf8'),"here22222------------------------------")
    #
    # context = {'result_value':response}
    # return render(request, 'waste_db/pay.html', context )

    context = {'result_value':request}
    return render(request, 'waste_db/KakaoPaySuccess.html', context )

########################
def home(request):
    return HttpResponse("Hello, Django!")

#사진 분류
def inceptionv3_inference(image_name):
    return run_inference_on_image(image_name)


# def image_post(request):
#     form = UploadFileForm()
#     if request.method == 'POST':
#         print(os.getcwd())
#         print("POST method")
#         print("request.POST : " + str(request.POST))
#         print("request.FILES : " + str(request.FILES))
#         form = UploadFileForm(request.POST, request.FILES)
#         print("dd")
#         if form.is_valid():
#             print("Valid")
#             for count, x in enumerate(request.FILES.getlist("files")):
#                 def handle_uploaded_file(f):
#                     with open(os.path.join(os.getcwd(),"waste/deep_learning/image", f.name),'wb+') as destination:
#                         for chunk in f.chunks():
#                             destination.write(chunk)
#                 handle_uploaded_file(x)
#                 print(x.name)
#                 #os.remove("media/"+str(x.name))
#                 #print(str(x.name)+"삭제완료")
#             context = {'form':form,}
#             return x.name
#             # return HttpResponse(" File uploaded! ")
#     else:
#         form = UploadFileForm()

#     return "false"


def save_image(f, f_name):
    with open(os.path.join(os.getcwd(),"waste/deep_learning/image", f_name),'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

        #os.remove("media/"+str(x.name))
        #print(str(x.name)+"삭제완료")
    return f_name

#request_data
#waste_type_name, waste_type_area_no
#response_data
#waste_type
def select_waste_type(request):
    #image_name = image_post(request)

    data = request.POST.get("data")
    data_dic = literal_eval(data)

    
    image_name = data_dic['file_name']
    #image decode
    imgstr = data_dic['files']
    imgstr += "=" * ((4 - len(imgstr) % 4) % 4)
    imgstr = imgstr.translate({ ord(' '): '+' })
    #logger.error(imgstr)
    image_data = ContentFile(base64.b64decode(imgstr), name=image_name)
    
    save_image(image_data, image_name)

    area_no = data_dic['area_no']
    if image_name != "false":
        #test
        list = []
        dic = {}
        dic['waste_type_no'] = 1
        dic['waste_type_waste_div_no'] = 1
        dic['waste_type_name'] = "ss"
        dic['waste_type_kor_name'] = "한국"
        dic['waste_type_size'] = "33"
        dic['waste_type_fee'] = "55"
        dic['waste_type_area_no'] = "1"
        list.append(dic)
        context = {'result_value':list}

        return render(request, 'waste_db/waste_type.html', context )

        #test
        #get image
        answer = inceptionv3_inference(image_name)
    else :
        print("image not found ERROR")
    
   # results = waste_type.objects.all()
   # data = request.GET.get("data")
   # data_dic = literal_eval(data)
    
    print("answer[0]['1_name'] : " + answer[0]['1_name'])
    #print(answer[0]['1_name'])
    #results = waste_type.objects.filter(waste_type_name=data_dic['waste_type_name'], waste_type_area_no=data_dic['waste_type_area_no'])
    results = waste_type.objects.filter(waste_type_name=answer[0]['1_name'], waste_type_area_no=area_no)
    
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
    data = request.POST.get("data")
    data_dic = literal_eval(data)

    #insert
    result = apply_info(apply_info_name=data_dic['apply_info_name'],
                        apply_info_address=data_dic['apply_info_address'],
                        apply_info_phone=data_dic['apply_info_phone'],
                        apply_info_waste_type_no=data_dic['apply_info_waste_type_no'],
                        apply_info_fee=data_dic['apply_info_fee'],
                        apply_info_code=data_dic['apply_info_code'],
                        apply_info_user_no=data_dic['apply_info_user_no'] )
    result.save()

    context = {'result_value':"success"}
    return render(request, 'waste_db/apply_info.html', context )

#request_data
#board_title, board_ctnt, board_user_no, board_waste_area_no

def insert_board(request):
    data = request.POST.get("data")
    data_dic = literal_eval(data)
    #current_time
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    #insert
    result = board(board_title=data_dic['board_title'],
                        board_ctnt=data_dic['board_ctnt'],
                        board_reg_user_no=data_dic['board_reg_user_no'],
                        board_reg_date=formatted_date,
                        board_waste_area_no=data_dic['board_area_no'] )
    result.save()

    context = {'result_value':"success"}
    return render(request, 'board_db/insert_board.html', context )

#response_data
#board_no, board_title, board_user_name, board_reg_date,board_waste_area_no
def select_board_title(request):
    
    results = board.objects.all()
    #results = waste_type.objects.filter(waste_type_name=data_dic['waste_type_name'], waste_type_area_no=data_dic['waste_type_area_no'])
    
    list = []
    for rst in results:
        
        dic = {}
        dic["board_no"] = rst.board_no
        dic['board_title'] = rst.board_title
        user_name = user_info.objects.filter(user_info_id=rst.board_reg_user_no)
        dic['board_user_name'] = user_name[0].user_info_name
        dic['board_reg_date'] = rst.board_reg_date
        dic['board_waste_area_no'] = rst.board_waste_area_no
        list.append(dic)
        
    context = {'result_value':list}
    return render(request, 'board_db/select_board_title.html', context )

#request_data
#board_no
#response_data
#board_no, board_title, board_user_name, board_reg_date,board_waste_area_no
def select_board(request):
    #results = waste_type.objects.all()
    data = request.POST.get("data")
    data_dic = literal_eval(data)
    results = board.objects.filter(board_no=data_dic['board_no'])
   
    list = []
    for rst in results:
        dic = {}
        dic['board_no'] = rst.board_no
        dic['board_title'] = rst.board_title
        dic['board_ctnt'] = rst.board_ctnt
        user_name = user_info.objects.filter(user_info_id=rst.board_reg_user_no)
        dic['board_user_name'] = user_name[0].user_info_name
        dic['board_reg_date'] = rst.board_reg_date
        dic['board_waste_area_no'] = rst.board_waste_area_no
        list.append(dic)
        
    context = {'result_value':list}
    return render(request, 'board_db/select_board.html', context )

#request_data
#board_no, board_reivew_ctnt, board_reivew_user_no,

def insert_board_review(request):
    data = request.POST.get("data")
    data_dic = literal_eval(data)
    #current_time
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    #insert
    result = board(board_review_board_no=data_dic['board_review_board_no'],
                        board_review_ctnt=data_dic['board_review_ctnt'],
                        board_review_reg_user_no=data_dic['board_review_reg_user_id'],
                        board_reg_date=formatted_date)
    result.save()

    context = {'result_value':"success"}
    return render(request, 'board_db/insert_board_review.html', context )

#response_data
#board_review_no, board_review_ctnt, board_review_user_name, board_review_reg_date
def select_board_review(request):
    #results = board.objects.all()
    data = request.POST.get("data")
    data_dic = literal_eval(data)
    results = board_review.objects.filter(board_review_board_no=data_dic['board_review_board_no'])
    
    list = []
    for rst in results:
        dic = {}
        dic['board_review_no'] = rst.board_review_no
        dic['board_review_ctnt'] = rst.board_review_ctnt
        user_name = user_info.objects.filter(user_info_id=rst.board_review_reg_user_no)
        dic['board_review_user_name'] = user_name[0].user_info_name
        dic['board_review_reg_date'] = rst.board_review_reg_date
        list.append(dic)
        
    context = {'result_value':list}
    return render(request, 'board_db/select_board_review.html', context )

#request_data
#user_info_no, user_info_id, user_info_name

def insert_user_info(request):
    data = request.POST.get("data")
    data_dic = literal_eval(data)
    #select
    results = user_info.objects.filter(user_info_id=data_dic['user_info_id'])
    for res in results:
        context = {'result_value':"success2"}
        return render(request, 'user_db/insert_user_info.html', context )
    else:
    #insert
        result = user_info(user_info_id=data_dic['user_info_id'],
                        user_info_name=data_dic['user_info_name'])
        result.save()
        context = {'result_value':"success"}
    return render(request, 'user_db/insert_user_info.html', context )

def test(request):
    data = request.POST.get("data")
  
    context = {'result_value':data}
    return render(request, 'user_db/test.html', context )
