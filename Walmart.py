import time, requests, json, lxml.html, multiprocessing
from Logger import configureLogger, getProcessNum, alert
from Phone import Phone

class Walmart:
    def __init__(self):
        pass

    def setLogger(self, logger):
        self.logger = logger

    def atc(self, productUrl, offerId):
        headers = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://www.walmart.com",
            "referer": productUrl,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
            "cookie": """vtc=Y1VF71Wd-NVT_Y5i3QQWTU; TS013ed49a=01538efd7c009ff161089043a3be1d7571294f90e0d60138cf5bb8d5cd89a83c971db738973ab7d7d7f7034af9c22f0f05d9975e5c; TBV=7; tb_sw_supported=true; tb_sw_registered=true; AID=wmlspartner%3D0%3Areflectorid%3D0000000000000000000000%3Alastupd%3D1586903434006; TS01a3099b=0130aff232bf139c1a60ee85e393c905d94b0820f669e046ab416e14d565f9fb2d218a72f5c263b001d51daa7ae90572504e33174a; brwsr=2c037073-7eb3-11ea-93cd-42010a246e0c; __cfduid=dfebf632b846d2e4215a442d7ca01d5de1587318510; type=GUEST; hasACID=1; hasCRT=1; nd_sess=0|1; TB_DNS_Perf_Test=1; TB_DC_Dist_Test=1; TB_DC_Flap_Test=1; bstc=Qh4hgpZhWFAn0uXit1Df_4; xpa=0w8xl|2e8Qh|2fUuZ|7viYL|9OWmX|HanY4|L-ChE|OSz3t|PPcYg|Ragpo|TabQF|aqToi|pVFdL; exp-ck=0w8xl12e8Qh12fUuZ17viYL19OWmX1HanY41L-ChE1OSz3t1PPcYg1Ragpo1TabQF1aqToi2pVFdL1; mobileweb=0; xpm=1%2B1587868055%2BY1VF71Wd-NVT_Y5i3QQWTU~%2B0; ndcache=b; akavpau_p3=1587869957~id=4366d5b572287e0b751f54502973e6f7; athrvi=RVI~h183ab566-h3b4b4a8b-h123da584-h205bf114-h20247e3d-h1754f9da-h2a4e52fb-h2021c13c-h304caee1; location-data=15213%3APittsburgh%3APA%3A%3A8%3A1|44b%2C1rd%2C45h%2C1zw%2C3w0%2C1rw%2C2ym%2C20b%2C3l0%2C41l||7|1|1y1w%3B16%3B0%2C1y1y%3B16%3B1%2C1y1k%3B16%3B2%2C1xzy%3B16%3B3%2C1y1x%3B16%3B4; DL=15213%2C%2C%2Cip%2C15213%2C%2C; t-loc-zip=1587869425852|15213; cart-item-count=0; pulse_oss=1; dfp_exp_8=buybox_reposition_controlA; TS01b0be75=01538efd7ca7925fcbd1c0577f03f8d1f8c443225d989c81e5ac904ff19764c9c397492c88f6a2b56acf4b102d64b456f3a600b258; next-day=1588006800|true|false|1588075200|1587870865; auth=MTAyOTYyMDE4xGqtso1bdkjdwBwIbvz9mpqdQ8Ajcjqnh%2FGSD%2FFfGtMLeSo62pxw%2FjRjhyREg%2B1MLkdeiYdvUCPcqE%2FJ2OMYJLX8Bx%2BJ4VOe%2B0KafIHhqZUgTZ1gkLwnaRx%2FlTUHE2lF767wuZloTfhm7Wk2KcjygobRHThsmZk%2BGcqTfIab85SmzIN%2FE%2B9UzJ%2FGhci8DMzfqa67OkSldPu3GrcxlxHv8rlIV0xva012e51OPAEvVBtGyEMqGry%2B0lIRqFvmUM8k0S4ks2VlT7qwuWkKDx%2Bp%2BMKQFGs8j4c5eWX%2BxjiKhQTrt48%2FvERiKpnV3HuPCC6MQ%2BtaKqYae6UFG4IgQ5MvHns%2FcB4RWUno4GJZ7kFhdZ%2FAvGJ5lEjFmlw4B7oxlFKnBNdMiHfAQM7sgkVhNkvnSQ%3D%3D; ACID=727977c5-a6bd-44de-b3d5-d781a11b586a; CRT=8bd41392-0d21-4521-bee3-ff89b50b108a; akavpau_p2=1587871466~id=38ed4d17379c7b3d0d8a5c03e4d75b4d; com.wm.reflector="reflectorid:0000000000000000000000@lastupd:1587870871170@firstcreate:1587870865713"; adblocked=true; TS011baee6=0130aff232f9fa2e934f562faf1efcd53f87298a9bc6325689d4f53d003ab0971f9650957b2df245d1ce6f70367f663f021a467dc3; TS01e3f36f=0130aff232f9fa2e934f562faf1efcd53f87298a9bc6325689d4f53d003ab0971f9650957b2df245d1ce6f70367f663f021a467dc3; TS018dc926=0130aff232f9fa2e934f562faf1efcd53f87298a9bc6325689d4f53d003ab0971f9650957b2df245d1ce6f70367f663f021a467dc3; akavpau_p8=1587871479~id=3c16809ff6cee2225d3805bf4093e443; akavpau_p0=1587871588~id=724662fa62c10973ba00ce657e58b65d"""
        }
        body = {"offerId": offerId, "quantity": 1}
        r = requests.post("https://www.walmart.com/api/v3/cart/guest/:CID/items", json=body, headers=headers,
                          timeout=30)
        if r.status_code == 200 and json.loads(r.text)["checkoutable"]:
            self.logger.info("ADDED TO CART!!!")
        else:
            self.logger.info(f"ERROR ATC ")

    def checkout(self, stopEvent):
        stopEvent.set()

    def monitor(self, productUrl, worker):
        self.setLogger(configureLogger(f"Walmart-{getProcessNum(multiprocessing.current_process().name)}"))

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
                    product = productUrl[27:productUrl[27:].find('/') + 27]
                    if "Add to cart" in response.text:
                        self.logger.info(f"walmart - {product} IN STOCK!!! sending message")
                        with worker.lock:
                            alert()
                            phone.sendMessage(productUrl)
                        doc = lxml.html.fromstring(response.text)
                        offerId = json.loads(doc.xpath('//script[@id="item"]/text()')[0])["item"]["product"]["buyBox"]["products"][0]["offerId"]
                        # self.atc(productUrl, offerId)
                        # self.checkout(worker.stopEvent)
                    # else:
                    #     self.logger.info(f"walmart - Out of stock for {product}!")
                except:
                    self.logger.exception("ERROR: could not send request!", exc_info=True)
                time.sleep(worker.checkTime.value)
        phone.close()
