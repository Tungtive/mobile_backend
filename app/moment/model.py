from flask_mongoengine import Document
from typing import Dict
from datetime import datetime
from ..user.model import User
from mongoengine.fields import (
    StringField,DateField,ReferenceField,ListField
)

class Moment(Document):
    
    user = ReferenceField('User')
    dateTime = DateField(default=datetime.now)
    context = StringField()
    imgUrl = ListField(StringField())


    def to_dict(self):
        return  {
            "id" :str(self.id),
            "user":{
               "username": self.user.username,
               "gender":self.user.gender,
               "age":self.user.gender,
               "unversity":self.user.university,
               "avatar_url":self.user.avatar_url
            },
            "datetime" : self.dateTime.isoformat(),
            "context":self.context,
            "imgUrl": self.imgUrl
        }