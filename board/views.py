from django.shortcuts import render, redirect
from board.models import Board, Comment
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlquote
import os
from django.http.response import HttpResponse, HttpResponseRedirect
from pip._internal import req


UPLOAD_DIR="D:/src/pyWeb/upload/" # file upload 폴더

# Create your views here.

def list(request):
    boardCount = Board.objects.count()
    boardList = Board.objects.all().order_by("-idx")
    
    # list.html: 템플릿 안?
    return render(request, "list.html",  
                  {"boardList": boardList, "boardCount": boardCount})

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
        
        
        
        
        
        
        
        
        
        