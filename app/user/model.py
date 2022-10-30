from typing import Dict

from flask_mongoengine import Document

from mongoengine.fields import (
    StringField,ListField,ReferenceField,FloatField
)

from ..utils import generate_s3_singed_url,compute_distance

# import bcrypt
# import base64
# import hashlib

# def get_hashed_password(plain_text_password):
#     return bcrypt.hashpw(
#         base64.b64encode(hashlib.sha256(plain_text_password.encode("utf-8")).digest()),
#         bcrypt.gensalt(),
#     ).decode("utf8")


# def check_password(plain_text_password, hashed_password):
#     return bcrypt.checkpw(
#         base64.b64encode(hashlib.sha256(plain_text_password.encode("utf-8")).digest()),
#         hashed_password.encode("utf8"),
#     )


class User(Document):

    username = StringField(required=True, unique=True, max_length=36)
    userID = StringField()
    password = StringField(required=True)
    phone_number = StringField()
    email  = StringField()
    gender = StringField()
    birth = StringField()
    height = StringField()
    status = StringField()
    university = StringField()
    sign = StringField()
    friends =  ListField(ReferenceField('User'))
    moments =  ListField(StringField())
    avatar_url = StringField()
    album = ListField(StringField())
    faculty = StringField()
    major = StringField()
    quiz  = ListField(StringField())
    loc = ListField(FloatField())
    def to_dict(self):
        return  {
            "id" :str(self.id),
            "userID": self.userID,
            "username":self.username,
            "password":self.password,
            "phone_number":self.phone_number,
            "gender":self.gender,
            "birth":self.birth,
            "status":self.status,
            "email":self.email,
            "university":self.university,
            "sign":self.sign,
            "friends": [friend.to_dict_friends(self.loc) for friend in self.friends],
            "height": self.height,
            "avatar_url":self.avatar_url,
            "album" : self.album,
            "faculty":self.faculty,
            "major":self.major,
            "quiz":self.quiz,
            "loc":self.loc

        }
    def to_dict_friends(self,loc):

        return {
            "username":self.username,
            "gender":self.gender,
            "university":self.university,
            "birth":self.birth,
            "sign":self.sign,
            "avatar_url": self.avatar_url,
            "distance": str(compute_distance(self.loc,loc))
        }


    # def __init__(self,user_id,user_name,user_mobile_number,user_email_address) -> 'User':
    #     self.id = user_id
    #     self.name = user_name
    #     self.mobile_number = user_mobile_number
    #     self.email_address  =  user_email_address
    # def to_dict(self) -> Dict:
    #     return{
    #         "id": self.id,
    #         "name": self.name,
    #         "mobile_number":self.mobile_number,
    #         "email_address":self.email_address
    #     }