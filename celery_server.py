import platform

from celery_app.server import app
from celery_app import config

if __name__ == "__main__":
    if platform.system() == "Windows":
        import multiprocessing

        worker_process = multiprocessing.Process(target=app.start, kwargs={
            "argv": ["worker", f"--loglevel={config.log_level}", "--pool=solo"]
        })
        worker_process.start()

        beats_process = multiprocessing.Process(target=app.start, kwargs={
            "argv": ["beat", f"--loglevel={config.log_level}"]
        })
        beats_process.start()

        worker_process.join()
        beats_process.join()
    else:
        app.start(
            argv=[
                "worker",
                "--beat",
                f"--loglevel={config.log_level}",
                "--pool=prefork"
            ]
        )
