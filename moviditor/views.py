from django.shortcuts import render, redirect
from django.http.response import HttpResponse
import os, io, zipfile
from . models import AudioModel, VideoModel
from . forms import AudioForm, ImageForm, VideoForm
from django.contrib import messages
import numpy as np
from .logic.file_handler import get_filefield_type, del_temp_files, audio_formats, video_formats
import moviditor.logic.movie as movie
from PIL import Image
from project_moviditor.settings import MEDIA_ROOT
from moviditor.logic.password import generator as gen
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .forms import FileFieldForm
# Create your views here.

# template folder path
tpath = os.path.abspath('moviditor\\templates\\moviditor')
'''the template path'''

os.makedirs(f'{MEDIA_ROOT}\\temp_files', exist_ok=True)
w_file_path = f'{MEDIA_ROOT}\\temp_files'
'''the path to write temp files'''


def home(request):
    '''the home view'''
    return render(request, f'{tpath}\\home.html')

@login_required(redirect_field_name='next')
def audio_view(request):
    '''view for fecthing user audio files'''
    audios = AudioModel.objects.filter(user=request.user).order_by('date_added')
    context = {"audios": audios}
    return render(request, f'{tpath}\\audios.html', context)

'''# class for handling multiple file uploads/ doesn't work
class FileFieldFormView(FormView):
    form_class = FileFieldForm
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def form_valid(self, form):
        files = form.cleaned_data['file_field']
        return (self.form_valid(), files)'''

@login_required(redirect_field_name="next")
def add_audio(request):
    '''view for uploading audio files'''
    if request.method != 'POST':
        form = AudioForm()
    else:
        form = AudioForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            audio = request.FILES['audio']
            # check if it is an audio type
            typ = get_filefield_type(audio)
            # get the extension of the file
            ext = audio.name
            ext = ext.split('.')
            ext = ext[-1]
            if 'audio' in typ and ext in audio_formats:
                new_audio = form.save(commit=False)
                new_audio.name = audio.name
                new_audio.user = request.user
                # covert audio.size(bytes) to megabytes
                byte_size = audio.size
                megabytes = np.divide(byte_size, 1_048_576)
                new_audio.size = megabytes
                new_audio.save()
                messages.success(request, f'{audio.name} has been successfully upload')
                return redirect('moviditor:audio', permanent=True)
            else:
                messages.error(request, f'{audio.name} is not a supported audio file')
                return redirect('moviditor:add-audio', permanent=True)
    context = {'form': form}
    return render(request, f'{tpath}\\add-audio.html', context)

@login_required(redirect_field_name="next")
def audio_to_mp4(request, audio_id):
    '''view for the converting audio to video, using an image'''
    audio = AudioModel.objects.get(id=audio_id)
    if request.method != 'POST':
        form = ImageForm()
    else:
        form = ImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            typ = get_filefield_type(image)
            if 'image' in typ:
                sound = audio.audio.path # audio file path
                # read temp_uploaded_img file, note that image will not be saved
                img_chunks = image.chunks() # chunks generator, .read() returns empty.
                # put all chunks into a single byte
                image_byte = b''
                for chunk in img_chunks:
                    image_byte += chunk
                # covert to numpy array using PIL.Image, to use in ImageClip
                # use BytesIO to feed entire image from single byte string
                image_obj = Image.open(io.BytesIO(image_byte))
                image_obj_rbg = image_obj.convert(image_obj.mode) # convert to usable mode
                image_arr = np.array(image_obj_rbg) # feed to numpy
                # feed data into video converter
                clip = movie.video_conv(sound, image_arr)
                a_name = audio.name
                w_name = a_name.split(sep='.mp3')
                name = w_name[0] # remove extension from name
                # write a new video file
                clip.write_videofile(f'{w_file_path}\\{name}.mp4', fps=30)
                file_path2 = f'{w_file_path}\\{name}.mp4' #video path
                file = open(file_path2, 'rb') # read video
                response = HttpResponse()
                response.content = file
                response['Content-Type'] = 'video/mp4'
                response['Content-Disposition'] = f'attachment; filename={name}.mp4'
                del_temp_files(file_path2)
                return response
            else:
                messages.error(request, 'an error occured, make sure image is correct.')
                return redirect('moviditor:convert-mp4', audio_id, permanent=True)     
    context = {'form': form, 'audio': audio}
    return render(request, f'{tpath}\\convert_mp4.html', context)

@login_required(redirect_field_name="next")
def video_view(request):
    '''view for fetching user's video files'''
    videos = VideoModel.objects.filter(user=request.user).order_by('date_added')
    context = {'videos': videos}
    return render(request, f'{tpath}\\videos.html', context)

@login_required(redirect_field_name="next")
def add_video(request):
    '''view for uploading video'''
    if request.method != 'POST':
        form = VideoForm()
    else:
        form = VideoForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            video = form.cleaned_data.get('video')
            typ = get_filefield_type(video)
            # get the extension of the file
            ext = video.name
            ext = ext.split('.')
            ext = ext[-1]
            if 'video' in typ and ext in video_formats:
                new_video = form.save(commit=False)
                new_video.name = video.name
                new_video.user = request.user
                # covert size to megabytes
                byte_size = video.size
                megabytes = np.divide(byte_size, 1_048_576)
                new_video.size = megabytes
                new_video.save()
                msg = f'{video.name} was uploaded successfully'
                messages.success(request, msg)
                return redirect('moviditor:video', permanent=True)
            else:
                msg = f'{video.name} is not a supported video file'
                messages.error(request, msg)
                return redirect('moviditor:add-video', permanent=True)
    context = {'form': form}
    return render(request, f'{tpath}\\add-video.html', context)

@login_required(redirect_field_name="next")
def cut_into_parts(request, video_id):
    '''view for splitting video into parts'''
    video_obj = VideoModel.objects.get(id=video_id)
    video_file = video_obj.video.path
    if request.method == 'GET':
        context = {'video': video_obj}
        return render(request, f'{tpath}\\cut_in_parts.html', context)
    else:
        number = request.POST['number']
        number = int(number)
        # write temp part videos
        try:
            video_list = movie.split_into_parts(video_file, number)
        except OSError:
            return HttpResponse(f'Your file "{video_obj.name}" is corrupt! BITCH')
        # a byte file that will contain the zipfile to be sent to user
        byt = io.BytesIO()
        # make zipfile to store videos, each time('w')
        zf = zipfile.ZipFile(byt, 'w')
        for video in video_list:
            file_path2 = f"{w_file_path}\\{video_list.index(video)}-{gen(4)}.mp4"
            video.write_videofile(file_path2)
            flname = os.path.basename(file_path2)
            zf.write(file_path2, flname)
            del_temp_files(file_path2)
        # close zipfile outside loop, after writing files into it
        zf.close()
        response = HttpResponse()
        # then get value of byt(the zipfile) in zf
        response.content = byt.getvalue()
        zip_file_name = f'{video_obj.name} part-cuts {gen(4)}.zip'
        response['Content-Type'] = 'application/x-zip-compressed'
        response['Content-Disposition'] = f'attachment; filename={zip_file_name}'
        return response

@login_required(redirect_field_name="next")    
def convert_mp3(request, video_id, video_name):
    '''view for converting video to mp3'''
    video = VideoModel.objects.get(name=video_name, id=video_id)
    if request.method != 'POST':
        # display video to be cut in html template
        context = {'video': video}
        return render(request, f'{tpath}//convert_mp3.html', context)
    else:
        # convert the video to audio/mp3
        video_path = video.video.path
        a_name = video.name
        b_name = a_name.split(sep='.mp4')
        name = b_name[0] # remove the extension of the file name/mp4
        # write audio file
        audio = movie.mp3_conv(video=video_path)
        audio.write_audiofile(f'{w_file_path}//{name}.mp3', nbytes=4, bitrate='3000k')
        content_path = f'{w_file_path}//{name}.mp3' #path to written audio file
        file = open(content_path, 'rb')
        response = HttpResponse(content=file) #create hhtpresponse obj
        response['Content-Type'] = 'audio/mpeg'
        response['Content-Disposition'] = f'attachment; filename={name}.mp3'
        del_temp_files(content_path)
        return response

@login_required(redirect_field_name="next")    
def timed_cut(request, video_id, video_name):
    '''view for splitting video into timed parts'''
    video = VideoModel.objects.get(name=video_name, id=video_id)
    if request.method != 'POST':
        context = {'video': video}
        return render(request, f'{tpath}\\timed_cut.html', context)
    else:
        time = request.POST['time']
        time = int(time)
        video_path = video.video.path # video file path
        # cut in timed parts and return list containing videos
        clip_list = movie.timed_cuts(video_path, time)
        byt = io.BytesIO() #buffer to store videos in zipfile
        zf = zipfile.ZipFile(byt, 'w')
        for w_clip in clip_list:
            # index for numbering files
            i = clip_list.index(w_clip)
            # path to write file to
            file_path2 = f'{w_file_path}\\{i}-{gen(4)}.mp4'
            name = os.path.basename(file_path2) # name for files in zip
            w_clip.write_videofile(file_path2) # write video file
            zf.write(file_path2, name) #write video file into byt zip
            del_temp_files(file_path2)
        zf.close()
        file = byt.getvalue()
        # get name for zipfile from original video file
        a_name = os.path.basename(video_path)
        b_name = a_name.split('.mp4')
        zf_name = b_name[0]
        # generate httpresponse
        response = HttpResponse(content=file)
        response['Content-Type'] = 'video/mp4'
        response['Content-Disposition'] = f'attachment; filename={zf_name}.zip'
        return response
        
@login_required(redirect_field_name="next")
def confirm_del_vid(request, video_id, video_name):
    '''view for confirming video deletion'''
    video = VideoModel.objects.get(name=video_name, id=video_id)
    context = {'video': video}
    return render(request, f'{tpath}\\confirm-video-del.html', context)

@login_required(redirect_field_name="next")
def del_video(request, video_id, video_name):
    '''view for deleting video'''
    if request.method != 'POST':
        video = VideoModel.objects.get(name=video_name, id=video_id)
        video_path = video.video.path
        del_temp_files(video_path)
        video.delete()
        messages.success(request, f'{video.name} was deleted successful.')
        return redirect('moviditor:video', permanent=True)
    else:
        raise Http404

@login_required(redirect_field_name="next") 
def confirm_audio_del(request, audio_id, audio_name):
    '''view for confirming audio deletion'''
    audio = AudioModel.objects.get(name=audio_name, id=audio_id)
    context = {'audio': audio}
    return render(request, f'{tpath}\\confirm-audio-del.html', context)

@login_required(redirect_field_name="next")
def del_audio(request, audio_id, audio_name):
    '''view for deleting audio'''
    if request.method != 'POST':
        audio = AudioModel.objects.get(name=audio_name, id=audio_id)
        audio_path = audio.audio.path
        del_temp_files(audio_path)
        audio.delete()
        messages.success(request, f'{audio.name} was deleted successful.')
        return redirect('moviditor:audio', permanent=True)
    else:
        raise Http404
    
def search(request):
    #fetch videos or/audios belonging to the user and contains the search phrase
    if request.method == 'POST':
        search_phrase = request.POST['search-phrase']
        audios = AudioModel.objects.filter(user=request.user
                                            ).filter(name__icontains=search_phrase
                                                    ).order_by('date_added')
        videos = VideoModel.objects.filter(user=request.user
                                        ).filter(name__icontains=search_phrase
                                                    ).order_by('date_added')
        context = {"audios": audios, 'videos': videos, 'phrase': search_phrase}
        return render(request, f'{tpath}\\search.html', context)
    else:
        return search(request)
        