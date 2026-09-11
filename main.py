import platform
import uvicorn
import multiprocessing

from typing import List

from app import config as app_config
from celery_app.server import app as celery_app
from celery_app import config as celery_config


if __name__ == "__main__":
    processes: List[multiprocessing.Process] = []

    if platform.system() == "Windows":
        worker_process = multiprocessing.Process(target=celery_app.start, kwargs={
            "argv": ["worker", f"--loglevel={celery_config.log_level}", "--pool=solo"]
        })
        worker_process.start()
        processes.append(worker_process)

        beats_process = multiprocessing.Process(target=celery_app.start, kwargs={
            "argv": ["beat", f"--loglevel={celery_config.log_level}"]
        })
        beats_process.start()
        processes.append(beats_process)

    else:
        celery_process = multiprocessing.Process(target=celery_app.start, kwargs={
            "argv": ["worker", "--beat", f"--loglevel={celery_config.log_level}", "--pool=prefork"]
        })
        celery_process.start()
        processes.append(celery_process)

    fastapi_process = multiprocessing.Process(target=uvicorn.run, kwargs={
        "app": "app.server:app",
        "host": app_config.listen_host,
        "port": app_config.listen_port,
        "log_level": app_config.log_level,
        "reload": app_config.reload_debug,
        "reload_dirs": ["app"],
    })

    fastapi_process.start()
    processes.append(fastapi_process)

    for process in processes:
        process.join()
