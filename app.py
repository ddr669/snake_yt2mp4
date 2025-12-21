from flask import Flask, render_template, request, url_for, send_file
from snake_yt2mp4 import get_video_values, mount_video
import json 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", display_="display: none;")

@app.route("/downloads/", methods=["POST"])
def get_video():
    '''
        TODO: token para acessar a pagina de download apenas quando houver requisição de video 
        Para evitar baixar diversas vezes mesmo só ao atualizar
    '''
	# TODO tratar request 
	
    req = request.form
	
	# integraçaõ com pytube
    linkzao = req["yt_url"]
    values = get_video_values(linkzao)
   
    return render_template("download_this.html", 
                           video_name=values['title'], 
                           video_thumb=values['thumb'],
                           author=values['autor'],
                           video_object=values['Object'],
                           FFCMD=values['FFCMD'],
                            display_="display: grid;")

@app.route("/now/", methods=["POST"])
def download_now():
    video_link = request.form
    _ = ""
    if "botao_download" in video_link:
        video = video_link['botao_download']
        video.replace("'", '"')
        print(video)
        video = json.loads(video.replace("'", '"'))    
        print(video)
		input("calabreso")
        mount_video(output_file=video['out'],video_file=video['video'], audio_file=video['audio'])
    
    return send_file(video['out'], as_attachment=True)
    

if __name__ == "__main__":
    app.run(debug=True)
