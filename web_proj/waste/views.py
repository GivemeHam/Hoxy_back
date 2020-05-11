from django.shortcuts import render

from django.http import HttpResponse

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


def save_image(image_data):
    def handle_uploaded_file(f):
        with open(os.path.join(os.getcwd(),"waste/deep_learning/image", "f_name.jpg"),'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    handle_uploaded_file(image_data)

            #os.remove("media/"+str(x.name))
            #print(str(x.name)+"삭제완료")
    return "f_name.jpg"

#request_data
#waste_type_name, waste_type_area_no
#response_data
#waste_type
def select_waste_type(request):
    #image_name = image_post(request)

    data = request.POST.get("data")
    data_dic = literal_eval(data)

    logger.error(data_dic['files'])
    #image decode
    image_data = ContentFile(base64.b64decode(data_dic['files']), name='temp.jpg')
    image_name = save_image(image_data)

    area_no = data_dic['area_no']
    if image_name != "false":
        #get image
        answer = inceptionv3_inference(image_name)
    else :
        print("image not found ERROR")
    
   # results = waste_type.objects.all()
   # data = request.GET.get("data")
   # data_dic = literal_eval(data)
    
    
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
        
    context = {'result_value':data_dic['files']}
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
                        board_user_no=data_dic['board_user_no'],
                        board_reg_date=formatted_date,
                        board_area_no=data_dic['board_area_no'] )
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
        user_name = user_info.objects.filter(user_info_no=rst.board_reg_user_no)
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
        user_name = user_info.objects.filter(user_info_no=rst.board_reg_user_no)
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
                        board_review_reg_user_no=data_dic['board_review_reg_user_no'],
                        board_reg_date=formatted_date)
    result.save()

    context = {'result_value':"success"}
    return render(request, 'board_db/insert_board_review.html', context )

#response_data
#board_review_no, board_review_ctnt, board_review_user_name, board_review_reg_date
def select_board_reivew(request):
    #results = board.objects.all()
    data = request.POST.get("data")
    data_dic = literal_eval(data)
    results = board_review.objects.filter(board_review_board_no=data_dic['board_review_board_no'])
    
    list = []
    for rst in results:
        dic = {}
        dic['board_review_no'] = rst.board_review_no
        dic['board_review_ctnt'] = rst.board_review_ctnt
        user_name = user_info.objects.filter(user_info_no=rst.board_review_reg_user_no)
        dic['board_review_user_name'] = user_name[0].user_info_name
        dic['board_review_reg_date'] = rst.board_review_reg_date
        list.append(dic)
        
    context = {'result_value':list}
    return render(request, 'board_db/select_board_review.html', context )

#request_data
#user_info_no, user_info_name

def insert_user_info(request):
    data = request.POST.get("data")
    data_dic = literal_eval(data)
    
    #insert
    result = user_info(user_info_no=data_dic['user_info_no'],
                        user_info_name=data_dic['user_info_name'])
    result.save()

    context = {'result_value':"success"}
    return render(request, 'user_db/insert_user_info.html', context )

def test(request):
    data = request.POST.get("data")
  
    context = {'result_value':data}
    return render(request, 'user_db/test.html', context )
