from flask import Flask, render_template, request, url_for, send_file
from snake_yt2mp4 import get_video_values, mount_video
import json 

app = Flask(__name__)



@app.route("/")
def home():
    return render_template("index.html", display_="display: none;")
@app.route("/downloads/", methods=["POST"])
def get_video():
    _dict_res = request.form
    linkzao = _dict_res["yt_url"] 
    #video, thumb = Download_youtube(linkzao)
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
        vi_ = video_link['botao_download']
       
        vi_.replace("'", '"')
        print(vi_)
        vi_ = json.loads(vi_.replace("'", '"'))    
        print(vi_)
        mount_video(output_file=vi_['out'],video_file=vi_['video'], audio_file=vi_['audio'])
    #aoba = video_link["values"]
    
    return send_file(vi_['out'], as_attachment=True)
    

if __name__ == "__main__":
    app.run(debug=True)