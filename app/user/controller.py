import datetime
from inspect import modulesbyfile
import json
from sys import stdout
from turtle import distance
from unittest import result
from xml.dom import UserDataHandler
from flask_restx import Namespace, Resource
from flask import jsonify, request

from uuid import uuid4
import requests
import ssl

from .model import User
from ..utils import upload_file_to_s3,generate_s3_singed_url,compute_distance
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
    
@api.route("/getUserByFilter")
class  GetUserByUserNameApi(Resource):
    def post(self):
        data =  request.json
        gender = data["gender"]
        status = data["status"]
        university = data["university"]
        age = data['age']
        if age!='':
            minAge = int(data["age"].split("-")[0])
            maxAge = int(data["age"].split("-")[1])

        today = datetime.datetime.today()
        year = int(today.year)
        month = int(today.month)
        day = int(today.day)
        results = []
        for user in User.objects():
            print(user.birth.split('/'))
            print(user.gender)
            print(user.status)
            print(user.university)
            if ((user.gender == gender) or gender=='') and ((user.status == status) or status =='')and ((user.university == university) or university == ''):
                if (age!=''):
                    gap = 0
                    print(user.birth.split('/'))
                    if (int(user.birth.split('/')[1])>month):
                        gap = -1     
                    if (int(user.birth.split('/')[1])==month) and (int(user.birth.split('/'))> day):
                        gap = -1
                    userYear = int(user.birth.split('/')[0])
                    age = year - userYear +gap 
                    if (age<=maxAge) and (age>=minAge):
                        user.avatar_url =  generate_s3_singed_url(user.avatar_url)
                        results.append(user)
                else : 
                    user.avatar_url =  generate_s3_singed_url(user.avatar_url)
                    results.append(user)
        return [re.to_dict() for re in results]
    
@api.route("/getUserFriends")
class  GetUserByUserNameApi(Resource):
    def post(self):
        data =  request.json
        user = User.objects(username = data['username']).first_or_404()
        friends = user.friends
        result = []
        for friend in friends:
            friend["avatar_url"] = generate_s3_singed_url(friend["avatar_url"])
            result.append(friend)

        return {"friends":[friend.to_dict_friends(user.loc) for friend in result]}

    
@api.route("/addFriend")
class  GetUserByUserNameApi(Resource):
    def post(self):
        data =  request.json
        user1 = User.objects(username = data['username1']).first_or_404()
        user2 = User.objects(username = data['username2']).first_or_404()
        for friend in user1.friends:
            if friend['username'] == user2.username:
                return {"message": user2.username+" already exist"}
        user1.friends.append(user2)
        user1.save()
        return {"user":user1.to_dict()}
    
@api.route("/deleteFriend")
class  GetUserByUserNameApi(Resource):
    def post(self):
        data =  request.json
        user1 = User.objects(username = data['username1']).first_or_404()
        user2 = User.objects(username = data['username2']).first_or_404()
        user1.friends.remove(user2)
        user1.save()
        return {"user":user1.to_dict()}

@api.route("/setSign")
class UsersetSign(Resource):
    def post(self):
        data = request.json
        user = User.objects(username = data['username']).first_or_404()
        user.sign = data["sign"]
        user.save()
        return {"user":user.to_dict()}

    
@api.route("/upLoadAvatar")
class userUploadAvatar(Resource):
    def post(self):
        uploaded_file = request.files.get("file")

        if uploaded_file is None:
            return {"message": "No file uploaded"}, 400


        username = request.form.get("username")
        user = User.objects(username = username).first_or_404()
        # Upload logic
    
        user.avatar_url = upload_file_to_s3(
            uploaded_file, f"users/avatars"
        )
        user.save()

        return {"username":user.username,"avatar_url":generate_s3_singed_url(user.avatar_url)}, 201

@api.route("/getUserAvatar")
class getUserAvatar(Resource):
    def post(self):
        username = request.json.get("username")
        user = User.objects(username = username).first_or_404()
        return {"username":username,"avatar_url":generate_s3_singed_url(user.avatar_url)},201
    


@api.route("/upLoadAlbum")
class userUploadAlbum(Resource):
    def post(self):
        uploaded_file = request.files.get("file")
        username =  request.files.get("username")
        if uploaded_file is None:
            return {"message": "No file uploaded"}, 400
        username = request.form.get("username")
        user = User.objects(username = username).first_or_404()
        # Upload logic
    
        img_url = upload_file_to_s3(
            uploaded_file, f"users/albums"
        )
        user.album.append(img_url)

        user.save()

        return {"upload":"sucess"}, 201

@api.route("/deleteUserAlbum")
class userUploadAlbum(Resource):
    def post(self):
        
        data = request.json
        username = data["username"]
        index = data["index"]
        user = User.objects(username = username).first_or_404()
        # Upload logic
        del user.album[int(index)]
        user.save()

        return {"delete":"sucess"}, 201

@api.route("/getUserAlbum")
class userUploadAlbum(Resource):
    def post(self):
        data = request.json
        user = User.objects(username = data['username']).first_or_404()
        imgUrlList = []
        for img_url in user.album:
            imgUrlList.append(generate_s3_singed_url(img_url))


        return {"username":user.username,"album":imgUrlList}, 201


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
        user.userID = str(len(User.objects())+1).zfill(7);
        user.password = data['password']
        user.phone_number = data['phone_number']
        user.email = data['email']
        user.gender = data['gender']
        user.status = data['status']
        user.birth = data["birth"]
        user.university = data["university"]
        user.height = data["height"]
        user.sign =data["sign"]
        user.faculty = data["faculty"]
        user.major = data["major"]
        user.avatar_url = "users/avatars/test.jpeg"
        user.quiz = data['quiz']
        user.loc = [-37.7983,144.9610]
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

@api.route("/updateUserLoc")
class UpdateUserLoc(Resource):
    def post(self):
        data = request.json
        username = data['username']
        loc = [float(i) for i in data['loc']]
        user = User.objects(username=username).first_or_404(message="User not found")
        user.loc = loc
        user.save()
        return {"x":str(user.loc[0]),"y":str(user.loc[1])}


@api.route("/updateUserQuiz")
class UpdateUserQuiz(Resource):  
    def post(self):
        data = request.json
        username = data['username']

        user = User.objects(username=username).first_or_404(message="User not found")
        user.quiz = data['quiz']
        user.save()
        return {"username":username,"quiz":user.quiz}


@api.route("/getDistance")
class getDistance(Resource):
    def post(self):
        data = request.json
        username1 = data['username1']
        username2 = data['username2']
       
        user1 = User.objects(username=username1).first_or_404(message="User not found")
        user2 = User.objects(username=username2).first_or_404(message="User not found")
        
        return {"distance":str(compute_distance(user1.loc,user2.loc))}
    
@api.route("/getUserByDistance")
class getUserByDistance(Resource):
    def post(self):
        data = request.json
        username = data['username']
        distance = data['distance']
        user = User.objects(username=username).first_or_404(message="User not found")
        result = []
        for user1 in User.objects():
            if (user1.to_dict()['username'] != username):
                dis = compute_distance(user.loc,user1.loc)
                if dis <= float(distance):
                    user1.avatar_url =  generate_s3_singed_url(user1.avatar_url)
                    result.append(user1)
        return [re.to_dict() for re in result]


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

@auth_api.route("/loginByPwd")
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

    

    

@auth_api.route("/loginBySms")
class loginBySms(Resource):
    def post(self):
        user = User.objects(phone_number=request.json.get('phone_num')).first_or_404(message="User not found")
        return {"user":user.to_dict(),"login":"ok"},201
    

@auth_api.route("/sendSms")
class sendSms(Resource):
    def post(self):
       
        phone_num = request.json.get('phone_num')
        host = 'https://miitangs09.market.alicloudapi.com'
        path = '/v1/tools/sms/code/sender'
        appcode = '25bdd1fc64094f0091b2a63bafbd0eaa'
        url = host + path

        payload = {'phoneNumber': phone_num,
                'smsSignId': '0000'}

        headers = {
            'Authorization': 'APPCODE ' + appcode,
            'X-Ca-Nonce': str(uuid4())
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.headers)
        # print(response.status_code)
        print(response.text)
        return {"response":json.loads(response.text)}
                