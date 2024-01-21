import subprocess
import datetime


def start_cron(username, interval, endtime):
    end_hour = int(endtime.split(":")[0]) + 12 - 1
    current_time = datetime.datetime.now().time()
    now = current_time.strftime("%H:%M")
    now_hour = int(now.split(":")[0])
    cron_job = f"*/{interval} {now_hour}-{end_hour} * * * /usr/bin/python3 /bis/source/cron_test.py >> /bis/cron_{username}.log 2>&1"
    subprocess.run(
        f'echo "{cron_job}" >> /etc/cron.d/cronjob',
        shell=True,
    )
    subprocess.run(f"chmod 0644 /etc/cron.d/cronjob", shell=True)
    subprocess.run(f"crontab /etc/cron.d/cronjob", shell=True)


def end_cron(username):
    subprocess.run(f"rm /bis/cron_{username}.log", shell=True)
    result = subprocess.run(f"crontab -l", stdout=subprocess.PIPE)
    crontab_content = result.stdout.decode()
    cron_jobs = crontab_content.strip().split("\n")
    for i in cron_jobs:
        if f"/bis/cron_{username}.log" in i:
            with open("/etc/cron.d/cronjob", "w") as f:
                f.write(crontab_content.replace(i, ""))


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
