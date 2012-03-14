import time
from   datetime import date

today     = date.today()
timestamp = today.strftime("%Y_%m_%d_%H_%M_%S")

NOT_RUN           = 0
RUNNING           = 1
FAILED            = 2
FINISH            = 3
STATUSES          = {}
STATUSES[NOT_RUN] = "'NOT RUN'"
STATUSES[RUNNING] = "'RUNNING'"
STATUSES[FAILED ] = "'FAILED'"
STATUSES[FINISH ] = "'FINISH'"
