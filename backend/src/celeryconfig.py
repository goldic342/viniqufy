# NOTE: celery config can't be stored in `config.py`, separate file is needed

broker_url = 'redis://localhost:6379'
result_backend = 'redis://localhost:6379/0'

imports = ('src.analysis.tasks',)

task_annotations = {
    'src.analysis.tasks': {'rate_limit': '100/m'}
}

task_track_started = True
