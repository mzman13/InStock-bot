import logging, os, winsound


def configureLogger(name):
    logger = logging.getLogger(name)
    logdir = os.path.join(os.getcwd(), "Logs")
    if not os.path.exists(logdir):
        try:
            os.makedirs(logdir)
        except Exception as e:
            print(f"ERROR: could not create logs dir - {e}")
    logfile = os.path.join(logdir, f"{name}.log")
    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s %(filename)s, line:%(lineno)d: %(message)s")
        filehandler = logging.FileHandler(logfile, mode='w')
        filehandler.setFormatter(formatter)
        stdouthandler = logging.StreamHandler()
        stdouthandler.setFormatter(formatter)
        logger.addHandler(filehandler)
        logger.addHandler(stdouthandler)
        logger.setLevel(logging.INFO)
    return logger

def getProcessNum(processName):
    if processName == 'MainProcess':
        num = 0
    else:
        num = int(processName[processName.find('-')+1:]) - 1
        if num < 0:
            print("ERROR: negative process number!")
            num += 1
    return num

def alert():
    winsound.Beep(1500, 1000)
