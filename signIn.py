# -*- encoding=utf-8 -*-

from libapi import *


a =[{"username": "2","password": ""},
        {"username": "","password": "1"}]


def logIn(each):	
    try:
	user = libapi(each["username"], each["password"])	
    except:
	user = logIn(each)
    return user


for each in a:
    user = logIn(each)
    user.checkIn()



