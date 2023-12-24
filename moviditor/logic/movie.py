'''a module that utilizes moviepy library to edit videos and audio'''
import moviepy.editor as mpy

def cut(m_clip, b, e):
        """a funcution to cut video(m_clip)
        and returns the 'w_clip'
        in specified b(mins), e(secs).\n
        Note: use w_clip.write_videofile(f"{path}\\/{name}.mp4")
        to write file"""
        with mpy.VideoFileClip(m_clip) as cl:
            clip = cl
        w_clip = clip.subclip(b, e)
        return w_clip

def split_into_parts(mn_clip, st: int) -> list:
    '''a function that takes a clip a returns a list = [w_clip,...]:
    each w_clip is a specified num of parts/st(split time) given.
    m_clip(main clip), st(split time)\n
    i.e, mn_clip = 30 sec, with st(3) -> 10 sec clip in 3 places.\n
    Note: iterate over list,
    and use w_clip.write_videofile(f"{path}\\/{i}/{name}.mp4")
    to write file. *i is item index in list'''
    m_clip =  mpy.VideoFileClip(mn_clip)
    clip_duration = m_clip.duration
    #calculate how long each part is
    parts = clip_duration / st
    # create list to store clips to return
    pack = list()
    # save parts, works.
    for i in range (st):
        b = i * parts
        e = (1 + i) * parts if i < st else clip_duration
        w_clip = m_clip.subclip(b, e)
        pack.append(w_clip)
    return pack
    
def mp3_conv(video):
    '''a function that converts a video into mp3.
    and returns the audio.\n
    Note: use audio.write_audiofile(nbytes=4, bitrate='3000k')
    to write files'''
    p_video = mpy.VideoFileClip(video)
    # get the audio
    audio = p_video.audio
    return audio

def timed_cuts(video, tp) -> list:
    '''splits a video into timed parts\n
    i.e, video(30s) with tp(10s), with produce
    a video list of 10s per video.\n
    Note: iterate over list,
    and use w_clip.write_videofile(f"{path}\\/{i}/{name}.mp4")
    to write file. *i is item index in list'''
    clip =  mpy.VideoFileClip(video)
    duration = clip.duration
    # list to store timed parts
    pack = list()
    # split into timed parts(tp)
    b = 0
    e = tp
    count = 1
    while b < duration:
        w_clip = clip.subclip(b, e)
        pack.append(w_clip)
        b += tp
        e += tp
        count += 1
        if e > duration:
            e = duration
            w_clip = clip.subclip(b, e)
            pack.append(w_clip)
            break
    return pack

def video_conv(audio, img):
    '''a function for convert audio into videos
    with the img(image).\n
    Note: use clip.write_videofile(f"{path}\\/{name}.mp4", fps=30)'''
    sound = mpy.AudioFileClip(audio)
    clip =  mpy.ImageClip(img, ismask=False)
    clip.audio = sound
    clip.duration = sound.duration
    return clip
