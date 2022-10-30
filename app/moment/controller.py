from unittest import result
from app import user
from .model import Moment
from ..user.model import User
import json
from sys import stdout
from xml.dom import UserDataHandler
from flask_restx import Namespace, Resource
from flask import jsonify, request
from ..utils import upload_file_to_s3,generate_s3_singed_url
import copy
moment_api = Namespace('moment',description="users related api")

@moment_api.route("/")
class MomentListApi(Resource):
    def get(self):
        # return jsonify([user.to_dict() for user in user_db])
        result = []
        for  moment in  Moment.objects():
            temp = copy.copy(moment)
            temp.imgUrl = []
            if len(moment.imgUrl) > 0 :
                for img  in moment.imgUrl:
                    temp.imgUrl.append(generate_s3_singed_url(img))
            temp.user.avatar_url = generate_s3_singed_url( temp.user.avatar_url)
            result.append(temp)
            print(temp.to_dict())
        return [moment.to_dict()  for  moment in  result]

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
        moment.imgUrl = []
        moment.save()
        return {"moment":moment.to_dict(),"addMoment":"ok"},201



@moment_api.route("/addMomentWithImg")
class  AddMomentApi(Resource):
    def post(self):

        uploaded_files = request.files.getlist("file")
        
        if not uploaded_files :
            return {"message": "No file uploaded"}, 400
        username = request.form.get("username")
        context = request.form.get("context")
        moment =  Moment()
        # Upload logic
        imgList = []
        for file in uploaded_files:   
            img_url = upload_file_to_s3(
                file, f"users/moments"
            )
            imgList.append(img_url)
        moment.imgUrl = imgList
        user  =  User.objects(username = username).first_or_404()
        moment.user = user;
        moment.context = context
        moment.save()
        return {"moment":moment.to_dict(),"addMoment":"ok"},201

@moment_api.route("/getMomentByUsername")
class  GetMomentByUsername(Resource):
    def post(self):

        username = request.json.get("username")
        print(username)
        result = []
        for moment in Moment.objects():
            # print(moment.user.to_dict())
            if moment.user.to_dict()['username']==username:
                temp = copy.copy(moment)
                print(len(moment.imgUrl))
                if len(moment.imgUrl) > 0:
                    l = []
                    for img in moment.imgUrl:
                        l.append(generate_s3_singed_url(img))
                    temp.imgUrl = l
                temp.user.avatar_url = generate_s3_singed_url( temp.user.avatar_url)
                result.append(temp.to_dict())
        return {"username":username,"moments":result}
    
@moment_api.route("/deleteMoment")
class deleteMoment(Resource):
    def post(self):
        id = request.json.get('id') 
        moment  =  Moment.objects(id = id).first_or_404()
        Moment.objects(id=id).delete()

        return    {"message":"delete success"}   