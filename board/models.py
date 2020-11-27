from django.db import models
from datetime import datetime # datetime 사용할때 필요 
from pymongo.read_preferences import Primary
from bokeh.themes import default

# Create your models here. 테이블 생성하는 곳 

class Board(models.Model): # 게시판T
    idx = models.AutoField(primary_key=True) # 오토인크리먼트 p.k
    writer = models.CharField(null=False, max_length=50) # N.N
    title = models.CharField(null=False, max_length=200)
    content = models.TextField(null=False)
    hit = models.IntegerField(default=0)
    post_date = models.DateTimeField(default=datetime.now, blank=True)
    filename = models.CharField(null=True, blank=True, default="", max_length=500)
    filesize = models.IntegerField(default=0)
    down = models.IntegerField(default=0)
    
    
    def hit_up(self):
        self.hit += 1 # 게시글 읽을 때마다 올라감 
    def down_up(self):
        self.down += 1 # 파일 다운받을 때마다 올라감 
        
        
class Comment(models.Model): # 댓글T
    idx = models.AutoField(primary_key=True) # 오토인크리먼트 p.k
    board_idx = models.IntegerField(null=False)
    writer = models.CharField(null=False, max_length=50)
    content = models.TextField(null=False)
    post_date = models.DateTimeField(default=datetime.now, blank=True)
    
    
class Movie(models.Model): # 영화평점 리뷰 T
    idx=models.AutoField(primary_key=True)    
    title=models.CharField(null=False,max_length=500)
    content=models.TextField(null=False)
    point=models.IntegerField(default=0)
    
    
    
    
    
    
    
    
    
    
    
    