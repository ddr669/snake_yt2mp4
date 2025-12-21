# HTML Escaping  

[Reference flask in DOC](https://flask.palletsprojects.com/en/stable/quickstart/)  
  
  
When returning HTML (the default response type in Flask), any user-provided values rendered in the output must be escaped to protect from injection attacks. HTML templates rendered with Jinja, introduced later, will do this automatically.  
  
  
escape(), shown here, can be used manually. It is omitted in most examples for brevity, but you should always be aware of how you’re using untrusted data.  
  
  
>
> from flask import request  
> from markupsafe import escape  
> 
> @app.route("/hello")  
> def hello():  
>     name = request.args.get("name", "Flask")  
>     return f"Hello, {escape(name)}!"  


