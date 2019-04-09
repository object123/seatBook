# -*- encoding = utf-8 -*-


from libapi import *
import time
import json
from multiprocessing import Process

def checkRun(func):
    def wrapper(*arg):
        reu = func(*arg)
        with open('/home/ubuntu/seatBook/logs.dat', 'a') as fr:
            fr.write(func.__name__ + ' is runned!!\n')
            fr.close()
        return reu

    return wrapper


def timeLength(func):
    def wrapper(*arg):
        begin = time.time()
        Retu = func(*arg)
        end = time.time()
        timeLen = str(end - begin)
        with open('/home/ubuntu/seatBook/logs.dat', 'a') as fr:
            fr.write('the time of reserations:  '+ timeLen + 
                    '\n'+'=='*35+'\n')
            fr.close()
        return Retu
    return wrapper

@timeLength
def logIn(userList):
    Quser = []

    for each in userList:
        while True:
            try:
	        user = libapi(each["username"],each["password"])
            except:
	        continue
            else:
                Quser.append(user)
                break
    return Quser

    
@checkRun
def getWeek(): #get the day
    return int(time.strftime("%w"))

@checkRun
def jsonFile(filename):
    with open(filename, 'r') as seatFor:
        seatJson = json.load(seatFor)
    
    return seatJson

def writeLog(user, date, BOOL, filename2):
    log = user+':  '+BOOL+'\n' 
    
    with open(filename2, 'a') as fr:
        fr.write(log)
        fr.close()


@checkRun
def checkOpen(a):
    date = []
    while len(date)!=2:
        try:
            date = a.dates()
        except:
            continue
	else:
            time.sleep(1)
    with open('/home/ubuntu/seatBook/logs.dat', 
            'a') as fr:
        timeNow = time.ctime() 
        fr.write('the time of begin: '+timeNow+'\n')
        fr.close()
    
    return date

@timeLength
def reservation(Req, user, date, week, filename2):
    bookTime = user["time"][week]
    while True:
      	try: 
            Forma = Req.book(bookTime["begin"], bookTime["end"], 
	        	user["roomId"], user["seatNum"], date[1])
    	except:
            continue
	else:
	    break

    if Forma["status"]=="fail":
	while True:
	    try: 
                Forma = Req.book(bookTime["begin"], bookTime["end"], 
                        user["roomId"], user["seatNum2"], date[1])
    	    except:
		continue
	    else:
		break




    writeLog(user["username"], date[1], Forma["status"], filename2)



def bookSeat(Quser, userList, date, week, filename2):
    pros = []
    userLength =len(userList)
    for count in range(userLength):
        pro = Process(target=reservation, name='Book', 
                    args=(Quser[count], userList[count], date, week, filename2))
        pros.append(pro)
        pro.start()
    return True


def main():
    filename = '/home/ubuntu/seatBook/seat.json'
    filename2 = '/home/ubuntu/seatBook/logs.dat'
    week = getWeek()%7
    userList = jsonFile(filename)
    Quser = logIn(userList)
    date = checkOpen(Quser[2])
    bookSeat(Quser, userList, date, week, filename2)


if __name__ == '__main__':
    time.sleep(20)
    main()
