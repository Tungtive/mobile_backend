from .model import Moment
from ..user.model import User
import json
from sys import stdout
from xml.dom import UserDataHandler
from flask_restx import Namespace, Resource
from flask import jsonify, request

moment_api = Namespace('moment',description="users related api")

@moment_api.route("/")
class MomentListApi(Resource):
    def get(self):
        # return jsonify([user.to_dict() for user in user_db])
        return [moment.to_dict() for moment in  Moment.objects()]

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
        moment.save()
        return {"moment":moment.to_dict(),"addMoment":"ok"},201

@moment_api.route("/getMomentByUsername")
class  GetDataHistroyBynameApi(Resource):
    def post(self):

        username = request.json.get("username")
        result = []
        for moment in Moment.objects():
            if moment.user.to_dict()['username']==username:
                result.append(moment.to_dict())
        if len(result)== 0:
            return {"error":"empty moment data"}
        return result