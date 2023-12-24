'''define moviditor url paths'''
from django.urls import path
from . import views

app_name = 'moviditor'

urlpatterns=[
    path('', views.home, name='home'),
    path('audio', views.audio_view, name='audio'),
    path('add-audio', views.add_audio, name='add-audio'),
    path('convert-mp4/<int:audio_id>/', views.audio_to_mp4, name='convert-mp4'),
    path('video', views.video_view, name='video'),
    path('add-video', views.add_video, name='add-video'),
    path('cut-in-parts/<int:video_id>/', views.cut_into_parts, name='cut-in-parts'),
    path('confirm-del-video/<int:video_id>/<str:video_name>/', views.confirm_del_vid, name='confirm-del-vid'),
    path('del-video/<int:video_id>/<str:video_name>/', views.del_video, name='del-video'),
    path('confirm-del-audio/<int:audio_id>/<str:audio_name>', views.confirm_audio_del, name='confirm-del-aud'),
    path('del-audio/<int:audio_id>/<str:audio_name>/', views.del_audio, name='del-audio'),
    path('convert-to-mp3/<int:video_id>/<str:video_name>', views.convert_mp3, name='convert-to-mp3'),
    path('timed-cut/<int:video_id>/<str:video_name>/', views.timed_cut, name='timed-cut'),
    path('search', views.search, name='search'),
]
