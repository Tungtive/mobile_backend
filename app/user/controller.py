import datetime
import json
from sys import stdout
from xml.dom import UserDataHandler
from flask_restx import Namespace, Resource
from flask import jsonify, request

# from aliyunsdkcore.client import AcsClient
# from aliyunsdkcore.acs_exception.exceptions import ClientException
# from aliyunsdkcore.acs_exception.exceptions import ServerException
# from aliyunsdkcore.auth.credentials import AccessKeyCredential
# from aliyunsdkcore.auth.credentials import StsTokenCredential
# from aliyunsdkdysmsapi.request.v20170525.SendSmsRequest import SendSmsRequest

from .model import User

api = Namespace('user',description="users related api")




# user_db = [
#     User("1","Tom","18692077799","1194953762@qq.com"),
#     User("2","Jerry","0452663508","zunjiex@student.unimelb.edu.au")
# ]

@api.route("/")
class UserListApi(Resource):
    def get(self):
        # return jsonify([user.to_dict() for user in user_db])
        return [user.to_dict() for user in  User.objects()]


# def list_students():
#     if request.method == "GET":
#         return jsonify([student.to_dict() for student in student_db])
#     if request.method == "POST":
     

@api.route("/getUserByUsername")
class  GetUserByUserNameApi(Resource):
    def post(self):
        data =  request.json
        user = User.objects(username = data['username']).first_or_404()
        return {"user":user.to_dict()}
    
@api.route("/getUserFriends")
class  GetUserByUserNameApi(Resource):
    def post(self):
        data =  request.json
        user = User.objects(username = data['username']).first_or_404()

        return {"friends":user.to_dict()["friends"]}

    
@api.route("/addFriend")
class  GetUserByUserNameApi(Resource):
    def post(self):
        data =  request.json
        user1 = User.objects(username = data['username1']).first_or_404()
        user1.friends.append(data['username2'])
        user1.save()
        return {"user":user1.to_dict()}


@api.route("/register")
class  UserRegisterApi(Resource):
    def post(self):
        data =  request.json
        user = User()
        username  = data['username']
        for user1 in User.objects():
            if (user1.to_dict()['username']==username ): 
                return {"error":"username already exist!"},401
        user.username = username
        user.password = data['password']
        user.phone_number = data['phone_number']
        user.email = data['email']
        user.gender = data['gender']
        user.status = data['status']
        user.age = data["age"]
        user.university = data["university"]
        user.save()
        return {"user":user.to_dict(),"register":"ok"},201
# @api.route("/<user_id>")
# class UserApi(Resource):
#     def get(self, user_id):
#         # for user in user_db:
#         #     if user.id == user_id:
#         #         return user.to_dict()
#         # return "null", 404
#         return User.objects(id=user_id).first_or_404(message="User not found").to_dict()


@api.route("/updateUserInfo")
class  UserRegisterApi(Resource):
    def post(self):
        data =  request.json
        for user1 in User.objects():
            if (user1.to_dict()['username']==data['username'] ): 
                user = user1
                break
        if (data['password'] != ''):
            user.password = data['password']
        if (data['phone_number'] != ''):
            user.phone_number = data['phone_number']
        if (data['email'] != ''):
            user.email = data['email']
        if (data['status'] != ''):
            user.status = data['status']
        user.save()
        return {"user":user.to_dict(),"update user info":"ok"},201 

@api.route("/updateUserStatus")
class  UserRegisterApi(Resource):
    def post(self):
        data =  request.json
        for user1 in User.objects():
            if (user1.to_dict()['username']==data['username'] ): 
                user = user1
                break
        if (data['status'] != ''):
            user.status = data['status']
        user.save()
        return {"user":user.to_dict(),"update user status":"ok"},201   

auth_api = Namespace("auth")

@auth_api.route("/login")
class Login(Resource):
    def post(self):
        username = request.json.get("username")
        password = request.json.get("password")
        print(request.json)
        # if not username or not password:
        #     return {"error": "username or password is missing"}, 400
    
        user = User.objects(username=username).first_or_404(message="User not found")
        # if not check_password(password, user.password):
        #     return {"error": "password is incorrect"}, 401
        if user.password != password :
            return {"error": "password is incorrect"}, 401
        # jwt_token = create_access_token(
        #     identity=user.name, expires_delta=datetime.timedelta(days=30)
        # )
        return {"user": user.to_dict(),"login":"ok"}, 201

# @auth_api.route("/sms")
# class Sms(Resource):
#     def  post(self):
#         credentials = AccessKeyCredential('LTAI5tL1cxdWQgPoKqqFxd4D', 'h9UmT6yt5NTkBnajaweAtpyblPI3MM')
#         # use STS Token
#         # credentials = StsTokenCredential('<your-access-key-id>', '<your-access-key-secret>', '<your-sts-token>')
#         client = AcsClient(region_id='cn-hangzhou', credential=credentials)
#         phoneNum = request.json.get("phoneNumber")
#         smsRequest = SendSmsRequest()
#         smsRequest.set_accept_format('json')

#         smsRequest.set_SignName("阿里云短信测试")
#         smsRequest.set_TemplateCode("SMS_154950909")
#         smsRequest.set_PhoneNumbers(phoneNum)
#         smsRequest.set_TemplateParam("{\"code\":\"1234\"}")

#         smsResponse = client.do_action_with_exception(smsRequest)
#         # print(phoneNum)
#         code = json.loads(smsResponse.decode('utf8'))["Code"]
#         print(json.loads(smsResponse.decode('utf8'))["Code"])
        
#         return {"status":code}