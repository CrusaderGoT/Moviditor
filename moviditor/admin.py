from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from . models import AudioModel, VideoModel
from moviditor.logic.file_handler import del_temp_files

# Register your models here.

class AudioModelAdmin(admin.ModelAdmin):
    ''' the admin model class for the audiomodel that automatically saves the name and size'''
    model = AudioModel
    list_display = ('name', 'date_added', 'get_size_in_mb') #replaced size display to show it in mb
    def get_size_in_mb(self, obj):
        '''method for getting size with mb suffix'''
        if obj.size is not None:
            return f'{obj.size:.2f} MB'
        return 'N/A'
    get_size_in_mb.short_description = 'size (MB)'
    # method for saving name and size
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        # calculate size and name
        if obj.audio:
            obj.size = obj.audio.size / (1024 * 1024)
            obj.name = obj.audio.name
            obj.user = request.user
        else:
            obj.size = None
            obj.name = None
        return super().save_model(request, obj, form, change)
    def delete_model(self, request: HttpRequest, obj: Any) -> None:
        # when object is deleted, delete the video file also
        if request.method == 'POST':
            file_path = obj.audio.path
            print(file_path, 'this')
            del_temp_files(file_path)
        return super().delete_model(request, obj)
    def delete_queryset(self, request: HttpRequest, queryset: QuerySet[Any]) -> None:
        # delete multiple obj files that where deleted as a queryset
        if request.method == 'POST':
            for obj in queryset:
                file_path = obj.audio.path
                del_temp_files(file_path)
        return super().delete_queryset(request, queryset)
    
class VideoModelAdmin(admin.ModelAdmin):
    '''the admin model class for the videomodel that automatically saves the name and size'''
    model = VideoModel
    list_display = ('name', 'date_added', 'get_size_in_mb')
    def delete_model(self, request: HttpRequest, obj: Any) -> None:
        # when object is deleted, delete the video file also
        if request.method == 'POST':
            file_path = obj.video.path
            print(file_path, 'this')
            del_temp_files(file_path)
        return super().delete_model(request, obj)
    def delete_queryset(self, request: HttpRequest, queryset: QuerySet[Any]) -> None:
        # delete multiple obj files that where deleted as a queryset
        if request.method == 'POST':
            for obj in queryset:
                file_path = obj.video.path
                del_temp_files(file_path)
        return super().delete_queryset(request, queryset)
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if obj.video:
            obj.name = obj.video.name
            obj.size = obj.video.size / (1024 * 1024) #in mb
            obj.user = request.user
        else:
            obj.name = None
            obj.size = None
        return super().save_model(request, obj, form, change)
    def get_size_in_mb(self, obj):
        if obj.size is not None:
            return f'{obj.size:2f} MB'
        return 'N/A'
    get_size_in_mb.short_description = 'size (MB)'
        


    
# registered models
admin.site.register(AudioModel, AudioModelAdmin) 
admin.site.register(VideoModel, VideoModelAdmin)
