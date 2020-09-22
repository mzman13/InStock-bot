import smtplib, time, os, json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Phone:
    def __init__(self, logger):
        emailConfig = self.readEmailConfig()
        self.email = emailConfig['address']
        self.password = emailConfig['password']
        self.sms = self.getSMSAddress(emailConfig['phoneNumber'], emailConfig['provider'])
        self.smtp = "smtp.gmail.com"
        self.port = 587
        self.logger = logger
        self.destEmail = emailConfig['destEmail']

    def readEmailConfig(self):
        configFile = os.path.join(os.getcwd(), "config.json")
        with open(configFile) as f:
            data = json.load(f)
        return data['email']

    def getSMSAddress(self, number, provider):
        if provider == 'atnt':
            return f"{number}@txt.att.net"

    def startServer(self, timeToRun):
        try:
            # self.logger = configureLogger('phone')
            self.logger.info("connecting to email server and logging in")
            self.server = smtplib.SMTP(self.smtp, self.port, timeout=timeToRun+30)
            self.server.starttls()
            self.server.login(self.email, self.password)
            self.logger.info("logged in")
        except:
            self.logger.exception("ERROR: could not login to email server", exc_info=True)
            # sys.exit(1)

    def sendMessage(self, productUrl):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = self.sms
            msg['Subject'] = f"in stock!"
            body = f"{productUrl} in stock!"
            msg.attach(MIMEText(body, 'plain'))
            self.logger.info(f"sending text {body}")
            self.server.sendmail(self.email, self.sms, msg.as_string())
            if self.destEmail:
                self.logger.info(f"sending email")
                self.server.sendmail(self.email, self.destEmail, msg.as_string())
            time.sleep(1)
        except:
            self.logger.exception(f"ERROR: failed to send message for {productUrl}", exc_info=True)

    def close(self):
        try:
            self.logger.info("closing server connection")
            self.server.quit()
        except:
            self.logger.exception("ERROR: could not close email server connection", exc_info=True)
