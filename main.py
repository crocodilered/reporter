from datetime import date, datetime
from smtplib import SMTP_SSL

from celery import Celery
from celery.schedules import crontab
from loguru import logger

import config as c

app = Celery('reporter', broker=c.CELERY_BROKER_URL, task_acks_late=True)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    ct = crontab(hour=c.PERIODIC_TIME_HOURS, minute=c.PERIODIC_TIME_MINUTES)
    sender.add_periodic_task(ct, send_report.s())


@app.task()
def send_report():
    today_str = date.today().isoformat()
    report_path = c.REPORTS_PATH / f'{today_str}.txt'

    if not report_path.is_file():
        return

    with open(report_path, encoding='UTF-8') as f:
        report_content = f.read()

    now_str = datetime.now().strftime('%a, %d %b %Y  %H:%M:%S %Z')

    headers = {
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Transfer-Encoding': '8bit',
        'From': f'"{c.FROM_NAME}" <{c.FROM_ADDR}>',
        'Bcc': c.BCC_ADDR,
        'To': c.TO_ADDR,
        'Date': now_str,
        'X-Mailer': 'Mozilla Thunderbird',
        'Subject': f'Отчет {today_str}'
    }

    msg = ''

    for key, value in headers.items():
        msg += f'{key}: {value}\r\n'

    msg += f'\r\n\r\n{report_content}\r\n'

    try:
        cli = SMTP_SSL(host=c.SMTP_HOST, port=c.SMTP_PORT)
        cli.login(c.SMTP_LOGIN, c.SMTP_PASSWORD)
        cli.sendmail(
            c.FROM_ADDR,
            (c.TO_ADDR, c.BCC_ADDR),
            msg.encode(encoding='utf8')
        )
    except Exception as e:
        logger.error(f'Got error while app config: {type(e)} - {e}')
    else:
        logger.info(f'Report for {today_str} sent successfully.')


if __name__ == '__main__':
    send_report()
