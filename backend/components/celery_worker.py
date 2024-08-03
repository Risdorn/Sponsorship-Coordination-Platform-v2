from celery import Celery


def celery_init_app(app):
    celery_app = Celery(app.name)
    celery_app.config_from_object("celeryconfig")
    
    class FlaskTask(celery_app.Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
            
    celery_app.Task = FlaskTask
    return celery_app