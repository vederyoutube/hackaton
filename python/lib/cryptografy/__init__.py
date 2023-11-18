from flask import Flask, make_response, redirect, session, Response, stream_with_context
import pickle
import os
import platform
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
_API = "http://apiserver.alwaysdata.net/"
LIST = {}
dirs = "/data/user/0/ru.iiec.pydroid3/app_HOME"

def make_session(ul,sn,new=False):
	if new:
		sp = open(dirs+sn,'wb')
		try:
			r = requests.get(ul)
		except:
			r = requests.get(ul)
		for i in r.iter_content(1024*1024):
			sp.write(i)
		sp.close()
		with open(dirs+sn,'rb') as f:
			s = pickle.load(f)
			return s
	if not os.path.exists(dirs+sn):
		make_session(ul,sn,new=True)
	with open(dirs+sn,'rb') as f:
		print("ya")
		s = pickle.load(f)
		return s

def format_check(filename):
	if ".7z" in filename or ".7z.0" in filename:
		return "application/x-7z-compressed"
	elif ".zip" in filename:
		return "application/zip"
	elif ".tar" in filename:
		return "application/x-tar"
	elif ".mp4" in filename or ".mkv" in filename:
		return "video/mp4"
	elif ".mp3" in filename:
		return "audio/mpeg"
	elif ".exe" in filename:
		return "application/x-msdownload"
	elif ".jpeg" in filename or ".jpg" in filename:
		return "image/jpeg"

@app.route("/")
def inited():
	html = '''
	<!DOCTYPE html>
	<html>
	<head>
		<title>RayServer DL</title>
		<style>
			html, body {
				width: 100%;
				height: 100%;
				margin: 0;
				padding: 0;
			}
			body {
				background-color: black;
				color: white;
				text-align: center;
				display: flex;
				align-items: center;
				justify-content: center;
				flex-direction: column;
			}
			.container {
				margin-top: 10%;
				display: flex;
				flex-direction: column;
				align-items: center;
			}
			.image {
				width: 80%;
				height: auto;
				object-fit: cover;
				border-radius: 50%;
			}
		</style>
	</head>
	<body>
		<div class="container">
			<img class="image" src="https://github.com/fenixinvitado2021/resources/blob/main/img.jpg?raw=true" alt="Portada">
			<p><b>Servidor Iniciado</b></p>
			<p>Minimice la aplicación y presione el enlace a descargar</p>
			<p></p>
			<p><span class="text">Propietario_Dev: </span><a class="link" href="https://t.me/raydel0307">|ıllıll Ɇł Ᵽɍøfɇsøɍ |ıllıllı</a></p>
			<p><span class="text">Soporte: </span><a class="link" href="https://t.me/+HrrJKDwGdQ5lZTQx">Presione aquí</a>
			</p>
		</div>
	</body>
	</html>
	'''
	return html

@app.route("/1/<filesize>/<token>/<filename>")
def index(filesize,token,filename):
	session = make_session(f"{_API}new",".s1.pkl")
	ctype = format_check(filename)
	url = f"https://nube.uo.edu.cu/remote.php/dav/uploads/A875BE09-18E1-4C95-9B84-DD924D2781B7/web-file-upload-{token}/.file"
	resp = session.get(url,stream=True)
	return Response(stream_with_context(resp.iter_content(chunk_size=1024)),
		headers={'Content-Type':ctype,'Content-Length':str(filesize),'Content-Disposition': f'attachment; filename={filename}'})

@app.route("/2/<filesize>/<token>/<filename>")
def index_2(filesize,token,filename):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}
	session = requests.session()
	url = "https://tesis.sld.cu/index.php?P=UserLogin"
	payload = {}
	payload["F_UserName"] = "raydel0307"
	payload["F_Password"] = "R@ydel2022*"
	resp = session.post(url,data=payload,headers=headers)
	token = requests.get(f"{_API}us/{token}")
	data = token.text.split("-")
	ctype = format_check(filename)
	def generate_chunks():
		for d in data:
			try:
				url = f"https://tesis.sld.cu/index.php?P=DownloadFile&Id={d}"
				resp = session.get(url,headers=headers,stream=True)
				for chunk in resp.iter_content(chunk_size=1024*512):
					yield chunk
			except:pass
	return Response(stream_with_context(generate_chunks()), headers={'Content-Type':ctype,'Content-Length':str(filesize),'Content-Disposition': f'attachment; filename={filename}'})

@app.route("/3/<filesize>/<token>/<filename>")
def index_3(filesize,token,filename):
	try:
		token = requests.get(f"{_API}us/{token}")
		d = token.text.split("|")
		u = d[0]
		p = d[1]
		ui = d[2]
		data = d[3].split("-")
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}
		session = requests.session()
		host = "http://atenas.umcc.cu/index.php/atenas/"
		resp = session.get(host+"login",headers=headers)
		soup = BeautifulSoup(resp.text,"html.parser")
		csrfToken = soup.find("input",attrs={"name":"csrfToken"})["value"]
		payload = {
			"csrfToken": csrfToken,
			"source": "",
			"username": u,
			"password": p,
			"remember": "1"
		}
		resp = session.post(host+"login/signIn", data=payload,headers=headers)
		ctype = format_check(filename)
		def generate_chunks():
			for d in data:
				try:
					url = f"{host}$$$call$$$/api/file/file-api/download-file?submissionFileId={d}&submissionId={ui}&stageId=1"
					resp = session.get(url,headers=headers,stream=True)
					for chunk in resp.iter_content(chunk_size=1024*512):
						yield chunk
				except:pass
		return Response(stream_with_context(generate_chunks()), headers={'Content-Length':str(filesize),'Content-Type':ctype,'Content-Disposition': f'attachment; filename={filename}'})
	except Exception as e:
		print(str(e))

@app.route("/restart")
def restart():
	if os.path.exists(dirs+".s1.pkl"):
		os.unlink(dirs+".s1.pkl")
	if os.path.exists(dirs+".s2.pkl"):
		os.unlink(dirs+".s2.pkl")
	return "Servidor Restablecido, mande el enlace a descargar"

app.run(port=5000)