#!/bin/venv python
#-*-encode: utf-8-*-
#-*-
####################

from pytubefix import YouTube
from sys import argv 
from os import system, listdir
import subprocess as SUB
from random import randint

# 
def get_video_values(link):
    youtube_obj = YouTube(link, use_oauth=True, allow_oauth_cache=True)
    output = Download_youtube(youtube_obj)
    return {'title': youtube_obj.title,
            'autor': youtube_obj.author,
            'thumb': youtube_obj.thumbnail_url,
            'Object': youtube_obj,
            'FFCMD': output}

def mount_video(output_file: str,video_file: str, audio_file: str):
    
    video_file = f"mp4_files/separados/"+video_file
    audio_file = f"mp4_files/separados/"+audio_file
    # certifica de estar tudo correto 
    print(output_file, video_file, audio_file)

    # lista de strings para executar comando no ffmpeg
    ffmpeg_command = ["ffmpeg", "-y", "-i", f"{video_file}", "-i", f"{audio_file}", "-c", "copy", output_file]
    SUB.run(ffmpeg_command)
    # comando executando em background 
   

def Download_youtube(youtube_object: YouTube):
    
    # baixa audio e video separado para manter a qualidade do video
    video_stream = youtube_object.streams.filter(adaptive=True, file_extension="mp4", only_video=True).order_by("resolution").desc().first()
    audio_stream = youtube_object.streams.filter(adaptive=True, file_extension="mp4", only_audio=True).order_by("abr").desc().first()
    # limpa o titulo para evitar nomes impossiveis 
    titulo = youtube_object.title
    tit = ""
    for _ in titulo:
        _ = "_" if _ == " " else _
        tit += _.strip() if _ not in ["|", "/", "%", "\\", "$", "&", ".", ",", ";", ":", "?", "#", "&", "@"] else ""
    titulo = tit
    # sobrescreve o titulo com a variavel temporaria limpa 
    magic_number = f"{titulo.strip(" ")}"
    # numeros magicos para evitar sobrescrever videos e audios ! pode ser relevante ou não, tudo depende do intuito 
    if not video_stream or not audio_stream:
        print("Não foi possivel encontrar o video.")
        return -1
    # Arquivos de saida 
    # default path: mp4_files/output.mp4 | mp4_files/separados/audio.mp4 
    video_file = f"video_{magic_number}.mp4"
    audio_file = f"audio_{magic_number}.mp3"
    output_file = f"mp4_files/{titulo}.mp4"

    # faz o download para depois juntar com ffmpeg
    video_stream.download(output_path="mp4_files/separados", filename=video_file)
    audio_stream.download(output_path="mp4_files/separados", filename=audio_file)
    # excluir arquivos extras depois, não coloquei essa função por motivos de usar os arquivos de musica solta
    return {"out":output_file,"video":video_file,"audio":audio_file}
##################################
## não usado para o serviço http/web com flask 
def __help__():
    print("use:>  snake_yt2mp4.py https://youtube.com/watch?q=Whe34ad2")
    print()
    exit(0)

def main(url: str = None, out_path: str = "mp4_files"):
    print(url if url else __help__())
    _ = None
    try:
        _ = listdir(out_path)
    except FileNotFoundError:
        system(f"mkdir {out_path}")
    try:
        yt = YouTube(url)
        
        video_stream = yt.streams.get_highest_resolution()
        print(f"Downloading [{yt.title}]")
        video_stream.download(output_path=out_path)
        print("[*] Completed! [*] ")

    except Exception as Err:
        print(Err, "[!] Maybe the url doesnt exits [!] ")    

if __name__ == "__main__":
    try:
        if argv[1]:
            if argv[1] != "snake_yt2mp4.py":
                _link = argv[1]
                print(argv[1])
            else:
                try:
                    _link = argv[2]
                except IndexError:
                    __help__()
    except IndexError:
        _link = input("type the url:> ")
    
    app = main(_link)
