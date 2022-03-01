from django.apps import AppConfig


class WorkoutSessionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workout_session'

    def ready(self) -> None:
        import workout_session.signals
