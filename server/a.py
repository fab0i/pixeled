from tinydb import TinyDB, Query
from Alerts import NotificationAlert, CalendarAlert
import time

def process_jobs(db):
    Q = Query()
    jobs = db.search(Q.job == 'alert' and Q.soon <= 1)

    if not jobs:
        not1 = NotificationAlert(
            name="test1",
            stop={"condition": "date", "date": time.time() + 120},
            soon=0,
            date_start=time.time() + 3,
            display="image",
            display_info=None
        )
        db.insert(not1.to_dict())

        not2 = NotificationAlert(
            name="test2",
            stop={"condition": "date", "date": time.time() + 120},
            soon=1,
            date_start=time.time() + 6,
            display="image",
            display_info=None
        )
        db.insert(not2.to_dict())

        print("Inserted test jobs")
        jobs = db.search(Q.job == 'alert' and Q.soon <= 2)
        print(jobs)

    if len(jobs) == 0:
        return False
    elif len(jobs) == 1:
        job = jobs[0]
    else:
        # If there are more than 1 jobs to be executed in the next 5s, run the helper function to figure out which
        job = _get_job_to_execute(jobs)
    print(job)
    db.remove(Q.job == 'alert')


def _get_job_to_execute(jobs):
    """
    Given multiple jobs that are currently on the "soon" queue, returns the appropriate job to be executed. Logic:
    - If any job has soon=-1, return None, since a job is already queued for execution.
    - All jobs that have soon=1 have priority over jobs with soon=0, since new jobs that should be displayed on time.
    - For more than 1 job with soon=1, queue the one with oldest (min) date_start
    - For more than 1 job with soon=0, queue the one with oldest (min) last_run
    :param jobs:
    :return: job to be executed or None
    """

    min_job = None

    for job in jobs:
        # If we already have a job already queued for execution => We're not executing another one => return None
        if job['soon'] == -1:
            return None

        elif job['soon'] == 1:
            if not min_job or min_job['soon'] == 0 or job['date_start'] < min_job['date_start']:
                min_job = job

        elif job['soon'] == 0:
            if not min_job or (min_job['soon'] != 1 and job['last_run'] < min_job['last_run']):
                min_job = job

    return min_job


# scheduler.add_job(lambda: process_queue(db), trigger="interval", seconds=5)
db = TinyDB("./task_db.json")
process_jobs(db)