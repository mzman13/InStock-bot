import os, sys, time, multiprocessing, logging, json
from Logger import configureLogger
from BestBuy import BestBuy
from Walmart import Walmart
from Target import Target
from Gamestop import Gamestop
from Kohls import Kohls
from Costco import Costco
from SamsClub import SamsClub


class Worker:
    def __init__(self, checkTime, stopEvent, lock, timeToRun):
        self.checkTime = checkTime
        self.stopEvent = stopEvent
        self.lock = lock
        self.timeToRun = timeToRun * 60

def createBestBuyProcesses(productUrlsBestBuy, jobs, logger, bestBuyBot):
    apiLock = multiprocessing.Lock()
    for productUrl in productUrlsBestBuy:
        logger.info(f"starting process for {productUrl}")
        p = multiprocessing.Process(target=bestBuyBot.monitor, args=(productUrl, worker, apiLock,))
        p.start()
        jobs.append(p)

def createWalmartProcesses(productUrlsWalmart, jobs, logger, walmartBot):
    for productUrl in productUrlsWalmart:
        logger.info(f"starting process for {productUrl}")
        p = multiprocessing.Process(target=walmartBot.monitor, args=(productUrl, worker,))
        p.start()
        jobs.append(p)

def createTargetProcesses(productUrlsTarget, jobs, logger, targetBot):
    for productUrl in productUrlsTarget:
        logger.info(f"starting process for {productUrl}")
        p = multiprocessing.Process(target=targetBot.monitor, args=(productUrl, worker,))
        p.start()
        jobs.append(p)

def createGamestopProcesses(productUrlsGamestop, jobs, logger, gamestopBot):
    for productUrl in productUrlsGamestop:
        logger.info(f"starting process for {productUrl}")
        p = multiprocessing.Process(target=gamestopBot.monitor, args=(productUrl, worker,))
        p.start()
        jobs.append(p)

def createKohlsProcesses(productUrlsKohls, jobs, logger, kohlsBot):
    for productUrl in productUrlsKohls:
        logger.info(f"starting process for {productUrl}")
        p = multiprocessing.Process(target=kohlsBot.monitor, args=(productUrl, worker,))
        p.start()
        jobs.append(p)

def createSamsclubProcesses(productUrlsSamsclub, jobs, logger, samsclubBot):
    for productUrl in productUrlsSamsclub:
        logger.info(f"starting process for {productUrl}")
        p = multiprocessing.Process(target=samsclubBot.monitor, args=(productUrl, worker,))
        p.start()
        jobs.append(p)

def createCostcoProcesses(productUrlsCostco, jobs, logger, costcoBot):
    for productUrl in productUrlsCostco:
        logger.info(f"starting process for {productUrl}")
        p = multiprocessing.Process(target=costcoBot.monitor, args=(productUrl, worker,))
        p.start()
        jobs.append(p)

def test(worker, bestBuyBot, walmartBot, targetBot, gamestopBot, kohlsBot, costcoBot, samsclubBot):
    # productUrlsBestBuy = ["https://www.bestbuy.com/site/nintendo-switch-32gb-lite-yellow/6257142.p?skuId=6257142"]
    # bestBuyBot.monitor(productUrlsBestBuy[0], worker)

    productUrlsWalmart = ["https://www.walmart.com/ip/The-Legend-of-Zelda-Breath-of-the-Wild-Nintendo-Nintendo-Switch-045496590420/55432568"]
    walmartBot.monitor(productUrlsWalmart[0], worker)

    # productUrlsTarget = 'https://www.target.com/p/nintendo-switch-lite-yellow/-/A-77419249'
    # targetBot.monitor(productUrlsTarget, worker)

    # gamestopBot.monitor("https://www.gamestop.com/video-games/switch/games/products/pokemon-sword-expansion-pass-pokemon-shield-expansion-pass/11099665.html", worker)

    # kohlsBot.monitor("https://www.kohls.com/product/prd-2294858/lego-ninjago-shadow-of-ronin-for-nintendo-3ds.jsp?prdPV=32", worker)

    # samsclubBot.monitor("https://www.samsclub.com/p/nintendo-switch-neon-wireless-controller-case/prod23950667?pid=_Aff_LS&siteID=MfQy8kfx.Gk-bPezBTUrAz.HduntgJi.tg&ranMID=38733&ranEAID=MfQy8kfx*Gk&ranSiteID=MfQy8kfx.Gk-bPezBTUrAz.HduntgJi.tg", worker)

    # costcoBot.monitor("https://www.costco.com/nintendo-switch-pok%c3%a9mon-accessory-bundle.product.100524210.html", worker)

    # worker.phone.close()
    sys.exit(1)

if __name__ == '__main__':
    configFile = os.path.join(os.getcwd(), "config.json")
    with open(configFile) as f:
        data = json.load(f)

    jobs = []
    lock = multiprocessing.Lock()
    checkTime = multiprocessing.Value('i', data['checkTime'])
    stopEvent = multiprocessing.Event()
    timeToRun = data['timeToRun']
    logger = configureLogger('main')

    worker = Worker(checkTime, stopEvent, lock, timeToRun)
    bestBuyBot = BestBuy()
    walmartBot = Walmart()
    targetBot = Target()
    gamestopBot = Gamestop()
    kohlsBot = Kohls()
    costcoBot = Costco()
    samsclubBot = SamsClub()

    # test(worker, bestBuyBot, walmartBot, targetBot, gamestopBot, kohlsBot, costcoBot, samsclubBot)

    createBestBuyProcesses(data['bestbuy'], jobs, logger, bestBuyBot)
    createWalmartProcesses(data['walmart'], jobs, logger, walmartBot)
    createTargetProcesses(data['target'], jobs, logger, targetBot)
    createGamestopProcesses(data['gamestop'], jobs, logger, gamestopBot)
    createKohlsProcesses(data['kohls'], jobs, logger, kohlsBot)
    createSamsclubProcesses(data['samsclub'], jobs, logger, samsclubBot)
    createCostcoProcesses(data['costco'], jobs, logger, costcoBot)

    logger.info(f"sleeping for {timeToRun} min")
    time.sleep(timeToRun*60)
    logger.info("setting stop event!")
    stopEvent.set()
    for j in jobs:
        j.join()
    logging.shutdown()


# TODO: amazon
# TODO: set logs to debug level for easier debugging
# TODO: error handling - can't add to cart, only in store checkout, process fails
# TODO: add to cart
# TODO: clear cart once out of stock

# TODO?: checkout and stop program once bought
# TODO?: lock on checkout so 1 process buys at a time
# TODO?: how long is smtp connection open? starting phone server and sending message only while in stock
# TODO?: cant send api request, connections forcibly closed because timeout
