from django.shortcuts import render, redirect
from board.models import Board, Comment, Movie
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlquote
import os
from django.http.response import HttpResponse, HttpResponseRedirect
from pip._internal import req
from django.db.models import Q
import math
from board import bigdataPro
from django.db.models.aggregates import Avg
import pandas as pd

UPLOAD_DIR="D:/src/pyWeb/upload/" # file upload 폴더

# Create your views here.

def main(request):
    return render(request, "main.html")   

################################################################## 게시판 시작
def list1(request):
    boardCount = Board.objects.count()
    boardList = Board.objects.all().order_by("-idx")
    
    # list.html: 템플릿 안?
    return render(request, "list.html",  
                  {"boardList": boardList, "boardCount": boardCount})


@csrf_exempt # 데이터 저상 시 사용
def list(request):
    # 검색 옵션, 검색 값 
    try: #예외가 발생할 가능성이 있는 코드
        search_option = request.POST["search_option"]
    except: #예외가 발생했을 때의 코드
        search_option = "writer"
        
    try:
        search= request.POST["search"]
    except:
        search = ""
        
    # 필드명__contains=값: where 필드명 like '%값%'
    if search_option == "all":
        boardCount = Board.objects.filter(Q(writer__contains = search) |
                                          Q(title__contains = search) |
                                          Q(content__contains = search)).count()
    elif search_option == "writer":
        boardCount = Board.objects.filter(Q(writer__contains = search)).count()
    elif search_option == "title":
        boardCount = Board.objects.filter(Q(title__contains = search)).count()  
    elif search_option == "content":
        boardCount = Board.objects.filter(Q(content__contains = search)).count()  
        
    try:
        start = int(request.GET['start'])
    except:
        start = 0
    
    page_size = 10; # 페이지당 게시물수
    block_size = 3; # 한 화면에 표시할 페이지의 갯수
    end=start+page_size
    #전체 페이지 갯수 , math.ceil() 올림함수
    total_page=math.ceil(boardCount/page_size)
    #start 레코드시작번호 => 페이지번호
    current_page=math.ceil((start+1)/page_size)
    #페이지 블록의 시작번호, math.floor() 버림함수
    start_page=math.floor((current_page-1)/block_size)*block_size+1
    #페이지 블록의 끝번호
    end_page=start_page+block_size-1
    #마지막 페이지가 범위를 초과하지 않도록 처리
    if end_page>total_page:
        end_page=total_page
    
    if start_page>=block_size:
        prev_list=(start_page-2)*page_size
    else:
        prev_list=0
    
    if end_page<total_page:
        next_list=end_page*page_size
    else:
        next_list=0
    
    if search_option=="all":
        boardList=Board.objects.filter(Q(writer__contains=search) |
                                       Q(title__contains=search) |
                                       Q(content__contains=search)).order_by('-idx')[start:end]
    elif search_option=='writer':
        boardList=Board.objects.filter(writer__contains=search).order_by('-idx')[start:end]
    elif search_option=='title':
        boardList=Board.objects.filter(title__contains=search).order_by('-idx')[start:end]
    elif search_option=='content':
        boardList=Board.objects.filter(content__contains=search).order_by('-idx')[start:end]
    else:
        boardList=Board.objects.all().order_by('-idx')[start:end]
        
    links=[]
    # range(start_page,end_page+1) start_page~end_page
    # str(숫자변수) => 숫자변수를 스트링변수로
    for i in range(start_page, end_page+1):
        page_start=(i-1)*page_size
        links.append("<a class='page-link' href='?start="+ str(page_start) + "'>" + str(i) + "</a>")




    return render(request, "list.html",
                  {"boardList":boardList,
                   "boardCount":boardCount,
                   "search_option":search_option,
                   "search":search,
                   "range":range(start_page-1, end_page),
                   "start_page":start_page,
                   "end_page":end_page,
                   "block_size":block_size,
                   "total_page":total_page,
                   "priv_list":prev_list,
                   "next_list":next_list,
                   "links":links})


def write(request):
    return render(request, "write.html")


@csrf_exempt
def insert(request):
    fname = ""
    fsize = 0
    
    if "file" in request.FILES:
        file = request.FILES["file"]
        fname = file.name
        fsize = file.size
        fp = open("%s/%s" % (UPLOAD_DIR, fname), "wb")
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
    
    dto = Board(writer=request.POST["writer"], title=request.POST["title"],
                content=request.POST["content"], filename=fname, filesize=fsize)
    dto.save()
    print(dto)
    return redirect("/list")
   
    
def download(request):
    id = request.GET['idx']
    
    # select * from board_board where idx=id
    dto = Board.objects.get(idx=id)
    
    path = UPLOAD_DIR + dto.filename
    
    filename = os.path.basename(path)
    filename = urlquote(filename)
    
    with open(path, 'rb') as file:
        response = HttpResponse(file.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = "attachment;filename*=UTF-8''{0}".format(filename)
        dto.down_up()
        dto.save()
        return response
    
    
def detail(request):
    id = request.GET['idx']
    dto = Board.objects.get(idx=id)
    dto.hit_up()
    dto.save()
    
    commentList = Comment.objects.filter(board_idx=id).order_by("-idx")
    
    filesize = "%.2f"%(dto.filesize)
    return render(request, "detail.html", {"dto": dto, "filesize": filesize, "commentList": commentList})


@csrf_exempt
def update(request):
    id=request.POST['idx']
    dto_src=Board.objects.get(idx=id)
    fname=dto_src.filename
    fsize=0
    if "file" in request.FILES:
        file=request.FILES['file']
        fname=file.name
        fsize=file.size
        pf=open("%s%s"%(UPLOAD_DIR,fname),"wb")
        for chunk in file.chunks():
            pf.write(chunk)
        pf.close()
        
    dto_new=Board(idx=id,writer=request.POST['writer'],
                  title=request.POST['title'],
                  content=request.POST['content'],
                  filename=fname,filesize=fsize)
    dto_new.save()
    return redirect("/list")
    
    
@csrf_exempt
def delete(request):
    id=request.POST['idx']
    Board.objects.get(idx=id).delete()
    return redirect("/list")


@csrf_exempt
def reply_insert(request):
    id=request.POST['idx']
    dto=Comment(board_idx=id,
                writer=request.POST['writer'],
                content=request.POST['content'])
    dto.save()
    return HttpResponseRedirect("detail?idx=" + id)
 
 ################################################################## 게시판 끝       
        
    
################################################################## 영화 크롤링 시작

def movie_save(request):
    data=[]
    bigdataPro.movie_crawling(data)
    for row in data:
        dto=Movie(title=row[0],point=int(row[1]),content=row[2])
        dto.save()
    return redirect('/')
    
    
    
def chart(request):
    #sql='select title,avg(point) points from board_movie group by title'
    #data=Movie.objects.raw(sql)
    data=Movie.objects.values('title').annotate(point_avg=Avg('point'))[0:10]
    df=pd.DataFrame(data)
    bigdataPro.make_graph(df.title, df.point_avg)
    return render(request,"chart.html",{"data":data}) 
        
        