import logging

logger = logging.getLogger("RPA")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s -  %(lineno)d - %(levelname)s - %(message)s")
handler = logging.FileHandler('log.log', 'w')
handler.setFormatter(formatter)
logger.addHandler(handler)