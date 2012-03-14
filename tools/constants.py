from datetime import datetime


def getTimestampHighRes():
    tday = datetime.now()
    return tday.strftime("%Y_%m_%d_%H_%M_%S_%f")


def getTimestamp():
    tday = datetime.now()
    return tday.strftime("%Y_%m_%d_%H_%M_%S")

def getDatestamp():
    tday = datetime.now()
    return tday.strftime("%Y_%m_%d")

timestamp = getTimestamp()

NOT_RUN           = 0
RUNNING           = 1
FAILED            = 2
FINISH            = 3
STATUSES          = {}
STATUSES[NOT_RUN] = "'NOT RUN'"
STATUSES[RUNNING] = "'RUNNING'"
STATUSES[FAILED ] = "'FAILED'"
STATUSES[FINISH ] = "'FINISH'"

