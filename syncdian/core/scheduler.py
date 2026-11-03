import logging
from datetime import datetime
from typing import Optional, Callable

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from syncdian.config import get_config
from syncdian.constants import SCHEDULE_DAILY, SCHEDULE_INTERVAL
from syncdian.i18n import tr

logger = logging.getLogger(__name__)


class SchedulerService:
    JOB_ID = "syncdian_recurring_backup"

    def __init__(self, job_func: Callable[[], None]):
        self.config_manager = get_config()
        self.job_func = job_func
        self.scheduler = BackgroundScheduler(daemon=True)
        self._is_running = False

    def start(self):
        if not self._is_running:
            self.scheduler.start()
            self._is_running = True
            logger.info("Servicio de programación en segundo plano iniciado.")
        self.apply_schedule()

    def stop(self):
        if self._is_running:
            self.scheduler.shutdown(wait=False)
            self._is_running = False
            logger.info("Servicio de programación detenido.")

    def apply_schedule(self):
        """Aplica la configuración de programación actual."""
        cfg = self.config_manager.schedule

        # Eliminar trabajo existente si lo hubiera
        if self.scheduler.get_job(self.JOB_ID):
            self.scheduler.remove_job(self.JOB_ID)

        if not cfg.enabled:
            logger.info("Programación automática desactivada en configuración.")
            return

        if cfg.mode == SCHEDULE_DAILY:
            # Parsear "HH:MM"
            try:
                parts = cfg.daily_time.strip().split(":")
                hour = int(parts[0])
                minute = int(parts[1]) if len(parts) > 1 else 0
            except Exception:
                hour, minute = 21, 0

            trigger = CronTrigger(hour=hour, minute=minute)
            self.scheduler.add_job(
                self.job_func,
                trigger=trigger,
                id=self.JOB_ID,
                name=f"Syncdian Diario ({hour:02d}:{minute:02d})",
                replace_existing=True
            )
            logger.info(f"Programación diaria configurada: todos los días a las {hour:02d}:{minute:02d}")

        elif cfg.mode == SCHEDULE_INTERVAL:
            hours = max(1, cfg.interval_hours)
            trigger = IntervalTrigger(hours=hours)
            self.scheduler.add_job(
                self.job_func,
                trigger=trigger,
                id=self.JOB_ID,
                name=f"Syncdian Intervalo ({hours} horas)",
                replace_existing=True
            )
            logger.info(f"Programación por intervalo configurada: cada {hours} horas")

    def get_next_run_time(self) -> Optional[datetime]:
        """Obtiene la fecha y hora de la próxima ejecución programada."""
        job = self.scheduler.get_job(self.JOB_ID)
        if job and job.next_run_time:
            return job.next_run_time
        return None

    def get_next_run_formatted(self) -> str:
        next_dt = self.get_next_run_time()
        if not next_dt:
            if not self.config_manager.schedule.enabled:
                return tr("dash_schedule_disabled")
            return tr("dash_schedule_not_set")

        now = datetime.now(next_dt.tzinfo)
        if next_dt.date() == now.date():
            return tr("dash_next_today", time=next_dt.strftime("%H:%M"))
        return tr("dash_next_date", date=next_dt.strftime("%d/%m/%Y"), time=next_dt.strftime("%H:%M"))

