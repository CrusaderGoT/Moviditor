import magic
import os

def get_filefield_type(ff_obj):
    '''takes a file field object and returns its type'''
    big = ff_obj.multiple_chunks(chunk_size=5) #if bigger than 5mb returns true
    if big:
        file = ff_obj.temporary_file_path()
        magic_obj = magic.Magic(mime=True, keep_going=True)
        ff_type = magic_obj.from_file(file)
    else:
        chunks = ff_obj.chunks()
        file_chunk = b''
        for chunk in chunks:
            file_chunk += chunk
        magic_obj = magic.Magic(mime=True, keep_going=True)
        ff_type = magic_obj.from_buffer(file_chunk)
    return ff_type

def del_temp_files(file_path):
    'delete file in given path'
    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        print('path is not a file')
        pass

video_formats = [
    'mp4',
    'oog',
    'avi'
]

audio_formats = [
    'mp3',
    'wav',
]
