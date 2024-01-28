# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
from flask_cors import CORS
# creating a Flask app
app = Flask(__name__)
CORS(app)
import firebase_admin
from firebase_admin import credentials, db
cred = credentials.Certificate("cred.json")
firebase_admin.initialize_app(cred,{
	'databaseURL':'https://personal-portfolio-4dc7d-default-rtdb.asia-southeast1.firebasedatabase.app'
})
_ref = db.reference("/")


@app.route('/posts', methods = ['GET',"PATCH","DELETE"])
def Posts():
	if request.method=="GET":
		firebase_result = _ref.child("posts").get()
		response={
			"result":{}
		}

		for i in firebase_result:
			response["result"][i]=firebase_result[i]
		return response
	if request.method=="DELETE":
		if request.args.get("id"):
			id = request.args.get("id")
			firebase_result = _ref.child("posts").get()
			if firebase_result is not None:
				for x,y in firebase_result.items():
					if x==id:
						_ref.child("posts").child(x).set({})
						return "Deleted"
			return "data not found with given id "
		else:
			return 	"id not passed in request params"
	if request.method=="PATCH":
		data = request.json
		if request.args.get("id") and "title" in data:
			id = request.args.get("id")
			title = data["title"]
			firebase_result = _ref.child("posts").get()
			if firebase_result is not None:
				for x,y in firebase_result.items():
					if x==id:
						y["title"]=title
						_ref.child("posts").child(id).update({"title":title})
						if "linkedin_url" in data:
							y["linkedin_url"]=data["linkedin_url"]
							_ref.child("posts").child(id).update({"linkedin_url":data["linkedin_url"]})
						if "git_repo_url" in data:
							y["git_repo_url"]=data["git_repo_url"]
							_ref.child("posts").child(id).update({"git_repo_url":data["git_repo_url"]})
				return firebase_result
			else:
				return "id or title not passed in param not found in db"
		else:
			return "please pass the id in params"

@app.route('/posts', methods = ['POST'])
def add_posts():
	if request.method=="POST":
		data = request.json

		payload={}
		if "title" in data:
			payload["title"]=data["title"]
		if "linkedin_url" in data:
			payload["linkedin_url"]=data["linkedin_url"]
		if "git_repo_url" in data:
			payload["git_repo_url"]=data["git_repo_url"]
		status_data = _ref.child('posts').push(payload)

		firebase_result = _ref.child("posts").child(status_data.key).get()
		response={}

		for i in firebase_result:
			response["result"]={
				i:firebase_result[i]
			}
		return response
# driver function
if __name__ == '__main__':

	app.run(debug = True)
