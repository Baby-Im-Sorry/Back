import subprocess
import datetime

current_time = datetime.datetime.now().time()
formatted_time = current_time.strftime("%I:%M %p")


def test(user_id, interval, endtime):
    cron_job = f'*/{interval} * {formatted_time.split(":")[0]}-{endtime.split(":")[0]} * * * /usr/bin/python3 /bis/source/cron_test.py >> /bis/cron_test.log 2>&1'
    subprocess.run(
        f'echo "{cron_job}" > /etc/cron.d/cronjob_{user_id}',
        shell=True,
    )
    subprocess.run(f"chmod 0644 /etc/cron.d/cronjob_{user_id}", shell=True)
    subprocess.run(f"crontab /etc/cron.d/cronjob_{user_id}", shell=True)


# subprocess.run(["echo", f"hello_{formatted_time}"], shell=True)
# subprocess.run(["echo", "nice"], shell=True)
# subprocess.run(["echo", "legend"], shell=True)

# result = subprocess.run(
#     "echo hello; echo world", shell=True, capture_output=True, text=True
# )

# print(result.stdout)
