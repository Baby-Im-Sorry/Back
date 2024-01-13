import subprocess
import datetime

current_time = datetime.datetime.now().time()
formatted_time = current_time.strftime("%I:%M %p")


# def test(user_id, interval, endtime):
#     subprocess.run(
#         [
#             f'echo "*/{interval} * {formatted_time.split(":")[0]}-{endtime.split(":")[0]} * * * /usr/bin/python3 /bis/source/cron_test.py >> /bis/cron_test.log 2>&1" > /etc/cron.d/cronjob_{user_id} && chmod 0644 /etc/cron.d/cronjob_{user_id} && crontab /etc/cron.d/cronjob_{user_id}'
#         ],
#     )


def test(user_id, interval, endtime):
    subprocess.run(
        [
            f'echo "*/{interval} * {formatted_time.split(":")[0]}-{endtime.split(":")[0]} * * * /usr/bin/python3 /bis/source/cron_test.py >> /bis/cron_test.log 2>&1" > /etc/cron.d/cronjob_{user_id} && chmod 0644 /etc/cron.d/cronjob_{user_id} && crontab /etc/cron.d/cronjob_{user_id}'
        ],
    )
