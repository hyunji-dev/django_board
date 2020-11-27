from django.contrib import admin
from board.models import Board

# Register your models here.

class BoardAdmin(admin.ModelAdmin):
    list_display = ("idx", "title", "writer")
    
admin.site.register(Board, BoardAdmin)
