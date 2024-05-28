import logging as l
from logging import StreamHandler
from utils import envvars
import requests

class CustomLogHandler(StreamHandler):

    def __init__(self):
        StreamHandler.__init__(self)
        
    def emit(self, record):        
        message = "Информирую:"

        if record.levelname == 'WARNING':
            message = "Внимание!"
            
        elif (record.levelname == 'ERROR') or record.levelname == 'EXCEPTION' :        
            message = "Возникла ошибка!"                    
        
        elif record.levelname == 'CRITICAL':
            message = "Критический сбой в системе !!!"
        
        message += f"\n```{self.format(record)}```"    
        message = message.replace("_", "\_")
        message = message.replace("*", "\*")
        message = message.replace("[", "\[")
        #message = message.replace("`", "\`")
        message = message.replace("!", "\!")
        
        url = f"https://api.telegram.org/bot{envvars.BOT_TOKEN}/sendMessage"
        
        params = {
            "chat_id": envvars.MASTER,
            "text": message,
            "parse_mode":"MarkdownV2"
            }
        try:            
            resp = requests.post(url, params=params )
            if resp.status_code != 200:
                raise ValueError(f"Code: {resp.status_code} ::: {resp.json()['description']}")         

        except Exception as e:
            l.exception(f"Logging ::: message is not sended ::: \n { repr(e) }")
            

class Logger():
    def __init__(self) -> None:       
        l.basicConfig(
            level=l.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filename="logs.log"
        )
        self.logger = l.getLogger("lgr")        
        
        custom_handler = CustomLogHandler()
        custom_handler.setLevel(l.WARN)

        self.logger.addHandler(custom_handler)

    def inf(self,msg:str):
        self.logger.info(msg)
        
    def wrn(self,msg:str):
        self.logger.warning(msg)

    def exc(self,msg:str):
        self.logger.exception(msg)

    def err(self,msg:str):
        self.logger.error(msg)
        
    def crt(self,msg:str):
        self.logger.critical(msg)
        
logger = Logger()