from datetime import datetime, time

def isMktOpen():
    startTime = time(3, 30);        endTime = time(11, 30);    timeNow = datetime.utcnow().time()
    if startTime < timeNow < endTime:           return True
    else:                                       return False

if __name__ == "__main__":
    print(isMktOpen())
    