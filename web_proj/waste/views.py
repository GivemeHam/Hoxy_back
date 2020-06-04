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
import string
import random

@api_view(['POST'])
def KakaoPay(request):
    url = "https://kapi.kakao.com/v1/payment/ready"

#
    data=request.POST.get("data")
    data_dic=literal_eval(data)
    name=data_dic['name']
    total_fee=data_dic['total_fee']
    size=data_dic['size']
    user_name=data_dic['user_name']
#
    now = datetime.now()
    formatted_date = now.strftime('%Y%m%d%H%M%S')

    print(formatted_date,"1321312321313")

    print(name,total_fee,size,"77777777777")
    payload = "cid=TC0ONETIME&partner_order_id=1001&partner_user_id=gorany&item_name="+name+"&quantity="+size+"&total_amount="+total_fee+"&tax_free_amount=0&approval_url=http://172.16.16.136:8000/KakaoPaySuccess/?random="+formatted_date+user_name+"&cancel_url=http://172.16.16.136:8000/KakaoPayCancel/&fail_url=http://172.16.16.136:8000/KakaoPayFail/"
    payload.encode('UTF-8')
    headers = {'Authorization': 'KakaoAK 07bd56b63267b53895005b8792088d79','Content-Type': 'application/x-www-form-urlencoded','Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, headers=headers, data = payload.encode('UTF-8'))

    #print(response.text.encode('utf8'),"here------------------------------")
    json_string=response.text.encode('utf8')
    str_json=json_string.decode('utf-8')
    print("json_string : " +str_json)
    dict_json=json.loads(str_json)
    tid=dict_json['tid']
    #인증 쌍 만들기
    random=formatted_date+user_name
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
    print(type(request.GET.get("random")),"please!!!!!!!!",request.GET.get("random"))
    pg_token=request.GET.get("pg_token")
    date=request.GET.get("random")[0:13]
    user_name=request.GET.get("random")[14:]
    print("date=",date,"user_name",user_name+"ssssssssssssssssssssssssssssssssssoooooooooooooooooooooook")
    #db에서 가져옴
    results=forpay.objects.filter(random_no=request.GET.get("random"))
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
    response=response.json()
    response['code']=getRandomCode()
    
    print("durlsms!!!!!!!!!!!!!!!!!!!!!!!!!",response)
    # context = {'result_value':response}
    # return render(request, 'waste_db/pay.html', context )

    context = {'result_value':response}

    #todo : 결제 정보 db에 넣기
    
    return render(request, 'waste_db/KakaoPaySuccess.html', context )
##
def getRandomCode() :

    LENGTH = 12 # 12자리

    # 숫자 + 대소문자
    string_pool = string.ascii_uppercase + string.digits

    # 랜덤한 문자열 생성
    result = "" 
    for i in range(12) :
        result += random.choice(string_pool) # 랜덤한 문자열 하나 선택

    return result


##

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
        # #test
        # list = []
        # dic = {}
        # dic['waste_type_no'] = 1
        # dic['waste_type_waste_div_no'] = 1
        # dic['waste_type_name'] = "ss"
        # dic['waste_type_kor_name'] = "한국"
        # dic['waste_type_size'] = "33"
        # dic['waste_type_fee'] = "55"
        # dic['waste_type_area_no'] = "1"
        # list.append(dic)
        # context = {'result_value':list}

        # return render(request, 'waste_db/waste_type.html', context )

        # #test
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

def select_waste_type_top5(request):
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
        answer = inceptionv3_inference(image_name)
    else :
        print("image not found ERROR")
    
    print("answer[0]['1_name'] : " + answer[0]['1_name'])
    print("2 : " + answer[1]['2_name'])
    print("3 : " + answer[2]['3_name'])
    print("4 : " + answer[3]['4_name'])
    print("5 : " + answer[4]['5_name'])
    #print(answer[0]['1_name'])
    #results = waste_type.objects.filter(waste_type_name=data_dic['waste_type_name'], waste_type_area_no=data_dic['waste_type_area_no'])
    list = []
    for i in range(0,5) :
        results = waste_type.objects.filter(waste_type_name=answer[i][str(i+1)+'_name'], waste_type_area_no=area_no)
        for rst in results:
            dic = {}
            dic['waste_type_no'] = rst.waste_type_no
            dic['waste_type_waste_div_no'] = rst.waste_type_waste_div_no
            dic['waste_type_name'] = rst.waste_type_name
            dic['waste_type_kor_name'] = rst.waste_type_kor_name
            dic['waste_type_size'] = rst.waste_type_size
            dic['waste_type_fee'] = rst.waste_type_fee
            dic['waste_type_area_no'] = rst.waste_type_area_no
            dic['Top']=i+1
            list.append(dic)
            
    context = {'result_value':list}
    return render(request, 'waste_db/waste_type.html', context )

#request_data
#waste_type_name, waste_type_area_no

def insert_waste_apply_info(request):
    data = request.POST.get("data")
    data_dic = literal_eval(data)

    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    #insert
    result = apply_info(apply_info_name=data_dic['apply_info_name'],
                        apply_info_address=data_dic['apply_info_address'],
                        apply_info_phone=data_dic['apply_info_phone'],
                        apply_info_waste_type_no=data_dic['apply_info_waste_type_no'],
                        apply_info_fee=data_dic['apply_info_fee'],
                        apply_info_code=data_dic['apply_info_code'],
                        apply_info_user_no=data_dic['apply_info_user_no'],
                        apply_info_reg_date = formatted_date,
                        apply_info_total_size = data_dic['total_size'])
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

    #image
    data_dic['files'] = image_string_format(data_dic['files'])
    print("data_dic['files'] : " + data_dic['files'])
    if len(data_dic['files']) > 10:
        image_data = ContentFile(base64.b64decode(data_dic['files']), name=data_dic['file_name'])
        save_image(image_data, data_dic['file_name'])
    else:
        data_dic['file_name']='1'
        
         
    #insert
    result = board(board_title=data_dic['board_title'],
                        board_ctnt=data_dic['board_ctnt'],
                        board_reg_user_no=data_dic['board_reg_user_no'],
                        board_reg_date=formatted_date,
                        board_waste_area_no=data_dic['board_area_no'],
                        board_image_id=data_dic['file_name'])
    result.save()

    context = {'result_value':"success"}
    return render(request, 'board_db/insert_board.html', context )

def update_board(request):
    data = request.POST.get("data")
    print("data : " + data)
    data_dic = literal_eval(data)



    #update
    board_instance = board.objects.get(pk=data_dic['board_no'])
    board_instance.board_title=data_dic['board_title']
    board_instance.board_ctnt=data_dic['board_ctnt']
    board_instance.board_area_no=data_dic['board_area_no']
    board_instance.board_image_id=data_dic['file_name']
    data_dic['files'] = image_string_format(data_dic['files'])
    board_instance.save()
    
    #image
    print(len(data_dic['files']))
    if len(data_dic['files']) > 10:
        image_data = ContentFile(base64.b64decode(data_dic['files']), name=data_dic['file_name'])
        save_image(image_data, data_dic['file_name'])
    else:
        data_dic['file_name']='1'

    context = {'result_value':"success"}
    return render(request, 'board_db/update_board.html', context )

def delete_board(request):
    data = request.POST.get("data")
    data_dic = literal_eval(data)
    
    (board.objects.get(board_no=data_dic['board_no'])).delete()
    
    context = {'result_value':"success"}
    return render(request, 'board_db/delete_board.html', context )

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
    results = board.objects.filter(pk=data_dic['board_no'])[0]
    list = []
    dic = {}
    dic['board_no'] = results.board_no
    dic['board_title'] = results.board_title
    dic['board_ctnt'] = results.board_ctnt
    user_name = user_info.objects.filter(user_info_id=results.board_reg_user_no)
    dic['board_user_name'] = user_name[0].user_info_name
    dic['board_reg_date'] = results.board_reg_date
    dic['board_waste_area_no'] = results.board_waste_area_no
    dic['file_name'] = results.board_image_id
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
    result = board_review(board_review_board_no=data_dic['board_review_board_no'],
                        board_review_ctnt=data_dic['board_review_ctnt'],
                        board_review_reg_user_no=data_dic['board_review_reg_user_id'],
                        board_review_reg_date=formatted_date)
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
    if not results is None:
        context = {'result_value':"success2"}
        return render(request, 'user_db/insert_user_info.html', context )
    #insert
    result = user_info(user_info_id=data_dic['user_info_id'],
                        user_info_name=data_dic['user_info_name'])
    result.save()
    context = {'result_value':"success"}
    return render(request, 'user_db/insert_user_info.html', context )

#view image
def get_image(request):
    data = request.POST.get("data")
    data_dic = literal_eval(data)
    link = "waste/deep_learning/image/"+data_dic['image_name']

    # Get the image
    image = open(link, 'rb')
    image_read = image.read()

    # Get the Byte-Version of the image
    image_64_encode = base64.b64encode(image_read)

    # Convert it to a readable utf-8 code (a String)
    image_encoded = image_64_encode.decode('utf-8')
    context = {'result_value': image_encoded}
    return render(request, 'waste_db/get_image.html', context )


def select_waste_apply_info(request):
    #results = waste_type.objects.all()
    data = request.POST.get("data")
    data_dic = literal_eval(data)
    print("test : " + data_dic['user_no'])
    results = apply_info.objects.filter(apply_info_user_no=data_dic['user_no'])
    list = []

    for rst in results:
        dic = {}
        dic['apply_info_address'] = rst.apply_info_address
        waste_name = waste_type.objects.filter(waste_type_no=rst.apply_info_waste_type_no)[0]
        if rst.apply_info_total_size == "1" :
            dic['apply_info_waste_type_name'] = waste_name.waste_type_kor_name
        else :
            dic['apply_info_waste_type_name'] = waste_name.waste_type_kor_name + " 외 " + rst.apply_info_total_size-1 +"개"
            
        dic['apply_info_fee'] = rst.apply_info_fee
        dic['apply_info_code'] = rst.apply_info_code
        dic['apply_info_reg_date'] = rst.apply_info_reg_date
        list.append(dic)
        
    context = {'result_value':list}
    return render(request, 'waste_db/apply_info.html', context )



def image_string_format(str):
    imgstr = str
    imgstr += "=" * ((4 - len(imgstr) % 4) % 4)
    imgstr = imgstr.translate({ ord(' '): '+' })

    return imgstr

def test(request):
    data = request.POST.get("data")
  
    context = {'result_value':data}
    return render(request, 'user_db/test.html', context )
