import extractor
from threading import Thread
from api.models import Job
from apscheduler.schedulers.background import BackgroundScheduler


class QueueManager(object):
    def __init__(self):
        self.is_running = False
        self.current_job = None
        self.queue = []
        self.restore()

        scheduler = BackgroundScheduler()
        scheduler.add_job(self.poll, 'interval', seconds=15)
        scheduler.start()

    def enqueue(self, job):
        job.queued = True
        job.status = 'Queued'
        job.save()

        self.queue.append(job)

    def dequeue(self):
        next_job = None

        if len(self.queue) > 0:
            next_job = self.queue[0]
            del self.queue[0]

        return next_job

    def set_completed(self):
        if self.current_job is not None:
            self.is_running = False
            self.current_job = None

    def restore(self):
        for job in Job.objects.all().filter(complete=False):
            self.enqueue(job)

    def execute_next(self):
        if self.current_job is None and not self.is_running and len(self.queue) > 0:
            self.current_job = self.dequeue()
            self.current_job.queued = False
            self.current_job.save()

            thread = Thread(target=extractor.run_twitter, args=(self,))
            thread.start()

            self.is_running = True

    def poll(self):
        print("Polling. Jobs %d - Queue Manager" % (len(self.queue)))
        self.execute_next()

