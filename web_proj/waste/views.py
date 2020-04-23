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
from datetime import datetime

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
                        apply_info_user_no=data_dic['apply_info_user_no'] )
    result.save()

    context = {'result_value':"success"}
    return render(request, 'waste_db/apply_info.html', context )

#request_data
#board_title, board_ctnt, board_user_no, board_waste_area_no

def insert_board(request):
    data = request.GET.get("data")
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
    data = request.GET.get("data")
    data_dic = literal_eval(data)
    #results = waste_type.objects.filter(waste_type_name=data_dic['waste_type_name'], waste_type_area_no=data_dic['waste_type_area_no'])
    
    list = []
    for rst in results:
        dic = {}
        dic['board_no'] = rst.board_no
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
    data = request.GET.get("data")
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
    data = request.GET.get("data")
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
    data = request.GET.get("data")
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
