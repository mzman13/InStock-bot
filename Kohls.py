import time, requests, json, multiprocessing
from Logger import configureLogger, getProcessNum, alert
from Phone import Phone


class Kohls:
    def __init__(self):
        pass

    def setLogger(self, logger):
        self.logger = logger

    def atc(self, productUrl):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-length": "207",
            "content-type": "application/json",
            "cookie": """visitorId=0171BC8409740201A103DCB96B34DC65; sapphire=1; TealeafAkaSid=eQInIcIQnCbKprbxtoRGNTOgeOHuQ305; UserLocation=15213|40.430|-79.960|PA|US; adaptiveSessionId=A4118599616; criteo={}; UrCapture=94544973-1e11-61af-902a-aeff5209f346; fiatsCookie=DSI_2757|DSN_East%20Liberty|DSZ_15206; egsSessionId=892b8126-4be0-43f0-94df-4e67b17bcd0f; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJjZDI1NjJkZi02OWNkLTRiYjAtODg5YS0wNzNhNmEwODdkZjQiLCJpc3MiOiJNSTYiLCJleHAiOjE1ODgwOTIxMDQsImlhdCI6MTU4ODAwNTcwNCwianRpIjoiVEdULjdhZjc2YTlkYjEyNzRiYjY5MzM0NmEyOTQ1YTM5ZTJiLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6IjYyYzUwMmU2NmFmOGYxMWM5YzQ4ZmM5OTUwYTUzNjgxNWVhNjk0NzdkM2MzMWQwMjVmMTljNzliMTg2OTEwZTYiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.iCmzMr1RtExvYW1Ik4A-7GKugFnxuusOTCg6HdmN2NFQlK7VqEOD8Wu30qTuj4ZvkQLc-YbcIQaAL0pxitSBHHFejAeVWw8nlaxyUIajBCvcL1DUuT9kX2kNJNlBplgGoYgAqXT3gusqU6h7AMqLqgcoktt0Pz9fA5MLrhtby1a5Vyyga3zulguKkML2eIsJ-bTh-Syv5h2GsXz8GiEuji71ACI9BAaOkIKXca6v--x_pzPmDUNV83_X0mG1-x6SV-ZGsnCTb8qjUQ_No-HbmMJzt2S0tIBkISTWHPUjOo2HHh-YpNuFEI9t3MKTR7lBc3KGtF6VPoQ_j7Ped2j2Yg; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiJjZDI1NjJkZi02OWNkLTRiYjAtODg5YS0wNzNhNmEwODdkZjQiLCJpc3MiOiJNSTYiLCJleHAiOjE1ODgwOTIxMDQsImlhdCI6MTU4ODAwNTcwNCwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsfX0.; refreshToken=71s5bBut3eIa734167qIGHr-_ZQ-a_5OI3GbGOHWNOR3qFjv9TdPXR4w9nMGHrApwzcsLcbaII8A_hy4PiDRsA; guestType=G|1588005704000; tlThirdPartyIds=%7B%22pt%22%3A%22v2%3Aebaa4b8c945b2c1f3c59998a21b17ff373e9586aab8b020dfa98654177fa5cce%7Cc34d1e37526578043d0fbef3d809ade9216c4459bc3efc21885df5159ae8f461%22%2C%22adHubTS%22%3A%22Mon%20Apr%2027%202020%2012%3A41%3A47%20GMT-0400%20(Eastern%20Daylight%20Time)%22%7D; ci_pixmgr=other; ffsession={%22sessionHash%22:%221711231dac01f11588005706016%22%2C%22sessionHit%22:26%2C%22prevPageType%22:%22product%20details%22%2C%22prevPageName%22:%22video%20games:%20product%20detail%22%2C%22prevPageUrl%22:%22https://www.target.com/p/nintendo-switch-lite-yellow/-/A-77419249%22%2C%22prevSearchTerm%22:%22non-search%22}; targetMobileCookie=guestLogonId:null~guestDisplayName:null~guestHasVerifiedPhone:false""",
            "dnt": "1",
            "origin": "https://www.target.com",
            "referer": productUrl,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
        }
        url = "https://carts.target.com/web_checkouts/v1/cart_items?field_groups=CART%2CCART_ITEMS%2CSUMMARY&key=feaf228eb2777fd3eee0fd5192ae7107d6224b39"
        productId = productUrl[-8:]
        body = {"cart_type": "REGULAR", "channel_id": 10, "shopping_context": "DIGITAL",
                "cart_item": {"tcin": productId, "quantity": 1, "item_channel_id": "10"},
                "fulfillment": {"fulfillment_test_mode": "grocery_opu_team_member_test"}}
        r = requests.post(url, json=body, headers=headers, timeout=30)
        if r.status_code == 200 or r.status_code == 201:
            self.logger.info("ADDED TO CART!!!")
        else:
            self.logger.info(f"ERROR ATC ")

    def checkout(self, stopEvent):
        stopEvent.set()

    def monitor(self, productUrl, worker):
        self.setLogger(configureLogger(f"Kohls-{getProcessNum(multiprocessing.current_process().name)}"))

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
                    product = productUrl[42:productUrl[42:].find('.') + 42]
                    if 'isShipAvailable":true' in response.text:
                        self.logger.info(f"Kohls - {product} IN STOCK!!! sending message")
                        with worker.lock:
                            alert()
                            phone.sendMessage(productUrl)
                        # self.atc(productUrl)
                        # self.checkout(worker.stopEvent)
                    # else:
                    #     self.logger.info(f"Kohls - Out of stock for {product}!")
                except:
                    self.logger.exception("ERROR: could not send request!", exc_info=True)
                time.sleep(worker.checkTime.value)
