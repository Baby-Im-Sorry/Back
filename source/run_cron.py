import subprocess
import datetime

current_time = datetime.datetime.now().time()
now = current_time.strftime("%H:%M")
now_hour = int(now.split(":")[0])
now_minute = int(now.split(":")[1])


def run_cron(user_id, interval, endtime):
    end_hour = int(endtime.split(":")[0])
    cron_job = f"*/{interval} {now_hour}-{end_hour} * * * /usr/bin/python3 /bis/source/cron_test.py >> /bis/cron_test.log 2>&1"
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

# user_id = "test"
# interval = 10
# endtime = "1:00"
# end_hour = int(endtime.split(":")[0])
# # end_minute = int(endtime.split(":")[1].split(" ")[0])

# cron_job = f"*/{interval} {now_hour}-{end_hour} * * * /usr/bin/python3 /bis/source/cron_test.py >> /bis/cron_test.log 2>&1"
# subprocess.run(
#     f'echo "{cron_job}" > /etc/cron.d/cronjob_{user_id}',
#     shell=True,
# )
# print(f'echo "{cron_job}" > /etc/cron.d/cronjob_{user_id}')
