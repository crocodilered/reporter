from os import environ as e
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

try:
    # Celery broker connection
    CELERY_BROKER_URL: str = e['REPORTER_CELERY_BROKER_URL']
    # Periodic config
    x = e['REPORTER_PERIODIC_TIME'].split(':')
    PERIODIC_TIME_HOURS: int = int(x[0])
    PERIODIC_TIME_MINUTES: int = int(x[1])
    # Path where daily files with reports are
    REPORTS_PATH: Path = Path(e['REPORTER_REPORTS_PATH'])
    # SMTP connection
    SMTP_HOST: str = e['REPORTER_SMTP_HOST']
    SMTP_PORT: int = int(e['REPORTER_SMTP_PORT'])
    SMTP_LOGIN: str = e['REPORTER_SMTP_LOGIN']
    SMTP_PASSWORD: str = e['REPORTER_SMTP_PASSWORD']
    # Email config
    FROM_ADDR: str = e['REPORTER_FROM_ADDR']
    FROM_NAME: str = e['REPORTER_FROM_NAME']
    TO_ADDR: str = e['REPORTER_TO_ADDR']
    BCC_ADDR: str = e['REPORTER_BCC_ADDR']
except Exception as e:
    logger.critical(f'Got error while app config: {type(e)} - {e}')
    exit(1)
