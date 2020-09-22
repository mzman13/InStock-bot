import time, requests, json, multiprocessing
from Logger import configureLogger, getProcessNum, alert
from Phone import Phone

class BestBuy:
    def __init__(self):
        self.key = "p6Olr95wFBCT4tjnGRC4XGrV"

    def setLogger(self, logger):
        self.logger = logger

    def printResults(self, value):
        # self.logger.info(f"""{value['name']}
        # in store availability: {value['inStoreAvailability']} \n
        # in store availability text: {value['inStoreAvailabilityText']} \n
        # in store availability updated: {value['inStoreAvailabilityUpdateDate']} \n
        # online availability: {value['onlineAvailability']} \n
        # online availability text: {value['onlineAvailabilityText']} \n
        # online availability updated: {value['onlineAvailabilityUpdateDate']}
        try:
            self.logger.info(f"""{value['name']}
            online availability: {value['onlineAvailability']} \n
            online availability text: {value['onlineAvailabilityText']} \n
            online availability updated: {value['onlineAvailabilityUpdateDate']}
            {'-' * 20}""")
        except:
            self.logger.exception("ERROR: could not print", exc_info=True)

    def atc(self, productUrl, sku):
        headers = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-length": "31",
            "content-type": "application/json; charset=UTF-8",
            "origin": "https://www.bestbuy.com",
            "referer": productUrl,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
            "cookie": "oid=1380608209; CTT=69b892bf3aa4a42031e995c215a554bb; SID=2e97ca06-28f0-4141-8b13-1c88e997556d; UID=c7348080-c914-4425-9d09-f8a4619ad0f5; optimizelyEndUserId=oeu1587245301607r0.4251463557777493; COM_TEST_FIX=2020-04-18T21%3A28%3A22.426Z; locDestZip=15201; locStoreId=585; pst2=585; ZPLANK=83f9dd3a16164a149db024581fa94dc8; ui=1587686870461; G_ENABLED_IDPS=google; vt=a99b0535-85cd-11ea-8e4a-0a8044d0946d; pt=3425765840; DYN_USER_CONFIRM=1772a6aee39dcae321ba5f7195c348e8; DYN_USER_ID=ATG49361792310; physical_dma=508; ut=20f98590-85c0-11ea-9f0a-0aeba7490f21; at=eyJhY2Nlc3NUb2tlbiI6IllXTXRfOUwtRm9YVUVlcXVLQUJRVnE3bzZmSWNWc3M1aEdOLTRzTU90RUt3TUgtaVU0MHFBQUFBQUFBQUFBQSIsInRpbWVUb0xpdmUiOjE4MDAsImlzc3VlZFRpbWVzdGFtcCI6MTU4NzY5NjA0NTk4MCwiYXNzZXJ0aW9uIjoidTpjNW9WZ3BYMDFVV3ZWZlVPWDViTi1JRjg4R19ZVmVxcy1kamhwWVpBMUE4IiwicHJpbmNpcGFsIjoidTpjNW9WZ3BYMDFVV3ZWZlVPWDViTi1JRjg4R19ZVmVxcy1kamhwWVpBMUE4IiwicHJpbmNpcGFsSWRlbnRpZmllciI6IjIwZjk4NTkwLTg1YzAtMTFlYS05ZjBhLTBhZWJhNzQ5MGYyMSIsImNvbnN1bWFibGUiOmZhbHNlLCJ2ZXJzaW9uIjoiMS4wIn0.lMHsfaszkd3qxd_o_GJjhPSMHnzoTDvGTLIyYFlZyjgdhjXoyiBHwog5YSUfFYXBP61JYCbwK0RPhz_a68FqSQ; customerZipCode=15237|Y; _abck=B07801976675D206F9A374ED6EBD8F27~0~YAAQ3aUrF9VSs4dxAQAAUvskqgMEuO+TIYrjw2urR/EW5Ca7MRHR2fKXQC3PWyHwPWNK5/S9eMwx1Gt1GCo6BQOgP43v6YRQLPG2ONkwfEEU17qnz4dp0b5r2eVXknnRcyYgY0oDz/DUOP3TD6wEthH+zKl7j+3304vJgNW3TN32SnTtBQn9fYOpbZuKTna5CT72ucsqfR+eCHkmbX6XSLG1wNN5wMMj69pKr4pRCRe9TmP+ftMyw8rgVavT6Ajggsq54pewV5eTMAWHfJ2XJcWgFNSoLudSTHfwN6G8cB4KZ4eJhRUKr+nLSYTCSJNlqilV3A3sf2E=~-1~-1~-1; partner=198%26UBe0cIU37xyOTwU0TbWK8Xs3Uki2L1zBzWXnwA0%262020-04-25+17%3A22%3A46.189; ltc=10130; bm_sz=95A23EA2C900A0C09BCBCC082987D5B3~YAAQvqUrF6xI9IpxAQAA6pNvswcz96Jktc1+yToq2YcQiuRe07k1s7JW+MI9qmk50plkCJByrLtCty0pFEutVsNXI9iqdsyUf6KT+zks8WE6xpP4XVoDpRKt/89txktSCV9JJS9Ov1qJ+fJ1RsxaUjIEFNXX3Ro4eVbu0Yewi6nlYLgACE13/LWs8/vcVzYQvg==; bby_rdp=l; bby_cbc_lb=p-browse-e; bby_ispu_lb=p-ispu-e; bby_prc_lb=p-prc-e; bby_basket_lb=p-basket-e; bby_loc_lb=p-loc-e; CTE14=T; gvpHeaderFooterTransition=headerFooterGvp; cst_lb=p-cart-cloud; CartItemCount=0; basketTimestamp=1587853408118; sc-location-v2=%7B%22meta%22%3A%7B%22CreatedAt%22%3A%222020-04-18T21%3A29%3A01.869Z%22%2C%22ModifiedAt%22%3A%222020-04-25T22%3A23%3A34.833Z%22%2C%22ExpiresAt%22%3A%222021-04-25T22%3A23%3A34.833Z%22%7D%2C%22value%22%3A%22%7B%5C%22physical%5C%22%3A%7B%5C%22zipCode%5C%22%3A%5C%2215201%5C%22%2C%5C%22source%5C%22%3A%5C%22A%5C%22%2C%5C%22captureTime%5C%22%3A%5C%222020-04-25T22%3A23%3A34.447Z%5C%22%7D%2C%5C%22store%5C%22%3A%7B%5C%22zipCode%5C%22%3A%5C%2215237%5C%22%2C%5C%22searchZipCode%5C%22%3A%5C%2215201%5C%22%2C%5C%22storeId%5C%22%3A585%2C%5C%22storeHydratedCaptureTime%5C%22%3A%5C%222020-04-25T22%3A23%3A34.832Z%5C%22%2C%5C%22userToken%5C%22%3A%5C%2220f98590-85c0-11ea-9f0a-0aeba7490f21%5C%22%7D%2C%5C%22destination%5C%22%3A%7B%5C%22zipCode%5C%22%3A%5C%2215201%5C%22%7D%7D%22%7D"
        }
        body = {"items": [{"skuId": sku}]}
        r = requests.post("https://www.bestbuy.com/cart/api/v1/addToCart", json=body, headers=headers, timeout=30)
        if r.status_code == 200 and json.loads(r.text)["cartCount"] == 1:
            self.logger.info("ADDED TO CART!!!")
        else:
            self.logger.info(f"ERROR ATC {r.status_code} \n {r.content}")

    def checkout(self, stopEvent):
        stopEvent.set()

    def monitor(self, productUrl, worker, apiLock):
        processNum = getProcessNum(multiprocessing.current_process().name)
        self.setLogger(configureLogger(f"BestBuy-{processNum}"))

        phone = Phone(self.logger)
        phone.startServer(worker.timeToRun)

        sku = productUrl[productUrl.find('skuId=')+6:productUrl.find('skuId=')+6+7]
        url = f"https://api.bestbuy.com/v1/products/{sku}.json?apiKey={self.key}"

        while not worker.stopEvent.is_set():
        # for i in range(1):
            with requests.Session() as session:
                try:
                    with apiLock:
                        response = session.get(url, timeout=60)
                        time.sleep(0.5)
                    value = json.loads(response.text)
                    # self.printResults(value)

                    if value['onlineAvailability']:
                        self.logger.info(f"best buy - {value['name']} IN STOCK!!! sending message")
                        with worker.lock:
                            alert()
                            phone.sendMessage(productUrl)
                        # self.atc(productUrl, sku)
                        # self.checkout(worker.stopEvent)
                    # else:
                    #     self.logger.info(f"best buy - Out of stock for {value['name']}")
                except:
                    self.logger.exception("ERROR: could not send request!", exc_info=True)
                time.sleep(worker.checkTime.value)
        phone.close()
