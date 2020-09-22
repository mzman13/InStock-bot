import time, requests, json, multiprocessing
from Logger import configureLogger, getProcessNum, alert
from Phone import Phone


class Costco:
    def __init__(self):
        pass

    def setLogger(self, logger):
        self.logger = logger

    def monitor(self, productUrl, worker):
        self.setLogger(configureLogger(f"Costco-{getProcessNum(multiprocessing.current_process().name)}"))

        phone = Phone(self.logger)
        phone.startServer(worker.timeToRun)

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
        }

        while not worker.stopEvent.is_set():
        # for i in range(1):
            with requests.Session() as session:
                try:
                    response = session.get(productUrl, headers=headers, timeout=60)
                    product = productUrl[23:productUrl[23:].find('.') + 23]
                    if 'inventory" : "IN_STOCK' in response.text:
                        self.logger.info(f"Costco - {product} IN STOCK!!! sending message")
                        with worker.lock:
                            alert()
                            phone.sendMessage(productUrl)
                    # else:
                    #     self.logger.info(f"Costco - Out of stock for {product}!")
                except:
                    self.logger.exception("ERROR: could not send request!", exc_info=True)
                time.sleep(worker.checkTime.value)
