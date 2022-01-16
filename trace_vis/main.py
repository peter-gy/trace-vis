import json
import threading
import time

import loguru
import schedule

import trace_vis.service as service

targets: list[str] = [
    'google.com',
    'univie.ac.at',
    'facebook.com',
    'github.com',
    'twitter.com',
    'unsplash.com',
    'apple.com',
    'amazon.com',
    'wikipedia.org',
    'reddit.com',
]

output_file = 'trace_runs.json'


def run_targets():
    loguru.logger.debug(f'Running targets on thread {threading.current_thread()}')
    trace_run_dicts: list[dict] = [service.run_traceroute(target).as_dict() for target in targets]
    with open(output_file, 'a') as f:
        json.dump(trace_run_dicts, f, indent=2)
        f.write(',\n')


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


schedule.every(10).minutes.do(run_threaded, run_targets)

if __name__ == '__main__':
    loguru.logger.info('Starting trace_vis 🕵️‍️')
    # First run
    run_threaded(run_targets)
    while True:
        schedule.run_pending()
        time.sleep(1)
