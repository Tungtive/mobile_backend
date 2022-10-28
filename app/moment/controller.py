from app import user
from .model import Moment
from ..user.model import User
import json
from sys import stdout
from xml.dom import UserDataHandler
from flask_restx import Namespace, Resource
from flask import jsonify, request
from ..utils import upload_file_to_s3,generate_s3_singed_url
moment_api = Namespace('moment',description="users related api")

@moment_api.route("/")
class MomentListApi(Resource):
    def get(self):
        # return jsonify([user.to_dict() for user in user_db])
        for  moment in  Moment.objects():
            print(moment.to_dict())

        return [moment.to_dict()  for  moment in  Moment.objects()]

@moment_api.route("/addMoment")
class  AddMomentApi(Resource):
    def post(self):
        data =  request.json
        moment = Moment()
        print(data['username'])
        user  =  User.objects(username = data['username']).first_or_404()
        moment.user = user;
        print(user)
        moment.context = data['context']
        moment.imgUrl = ''
        moment.save()
        return {"moment":moment.to_dict(),"addMoment":"ok"},201



@moment_api.route("/addMomentWithImg")
class  AddMomentApi(Resource):
    def post(self):

        uploaded_file = request.files.get("file")
        
        if uploaded_file is None:
            return {"message": "No file uploaded"}, 400
        username = request.form.get("username")
        context = request.form.get("context")
        moment =  Moment()
        # Upload logic
        img_url = upload_file_to_s3(
            uploaded_file, f"users/moments"
        )
        moment.imgUrl = img_url
        user  =  User.objects(username = username).first_or_404()
        moment.user = user;
        moment.context = context
        moment.save()
        return {"moment":moment.to_dict(),"addMoment":"ok"},201

@moment_api.route("/getMomentByUsername")
class  GetDataHistroyBynameApi(Resource):
    def post(self):

        username = request.json.get("username")
        print(username)
        result = []
        for moment in Moment.objects():
            print(moment.user.to_dict())
            if moment.user.to_dict()['username']==username:
                temp = moment
                if temp.imgUrl != '':
                    temp.imgUrl = generate_s3_singed_url(moment.imgUrl)
                result.append(temp.to_dict())
        return result