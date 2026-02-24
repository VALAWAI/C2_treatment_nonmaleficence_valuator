#
# This file is part of the C2_treatment_nonmaleficence_valuator distribution
# (https://github.com/VALAWAI/c2_treatment_nonmaleficence_valuator).
# Copyright (c) 2022-2026 VALAWAI (https://valawai.eu/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import logging
import logging.config
import os
import signal

from c2_treatment_nonmaleficence_valuator.change_parameters_handler import ChangeParametersHandler
from c2_treatment_nonmaleficence_valuator.message_service import MessageService
from c2_treatment_nonmaleficence_valuator.mov import MOV
from c2_treatment_nonmaleficence_valuator.received_treatment_handler import ReceivedTreatmentHandler


class App:
    """The class used as application of the C2 Treatment nonmaleficence valuator."""

    def __init__(self):
        """Initialize the application"""
        self.message_service = None
        self.mov = None

        # Capture when the docker container is stopped
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, _signum, _frame):
        """Called when the docker container is closed"""
        self.stop()

    def stop(self):
        """Finalize the component."""
        try:
            if self.mov:
                self.mov.unregister_component()
            if self.message_service:
                self.message_service.close()
            logging.info("Finished C2 Treatment nonmaleficence valuator")
        except (OSError, ValueError):
            logging.exception("Could not stop the component")

    def start(self):
        """Initialize the component"""
        try:
            # Create connection to RabbitMQ
            self.message_service = MessageService()
            self.mov = MOV(self.message_service)

            # Create the handlers for the events
            ReceivedTreatmentHandler(self.message_service, self.mov)
            ChangeParametersHandler(self.message_service, self.mov)

            # Register the component
            self.mov.register_component()

            # Start to process the received events
            logging.info("Started C2 Treatment nonmaleficence valuator")
            self.message_service.start_consuming()

        except (OSError, ValueError):
            logging.exception("Could not start the component")



def configure_log():
    """Configure the logging system."""

    try:
        console_level = logging.getLevelName(os.getenv("LOG_CONSOLE_LEVEL", "INFO"))
        file_level = logging.getLevelName(os.getenv("LOG_FILE_LEVEL", "DEBUG"))
        file_max_bytes = int(os.getenv("LOG_FILE_MAX_BYTES", "1000000"))
        file_backup_count = int(os.getenv("LOG_FILE_BACKUP_COUNT", "5"))

        log_dir = os.getenv("LOG_DIR", "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file_name = os.path.join(log_dir, os.getenv("LOG_FILE_NAME", "c2_treatment_nonmaleficence_valuator.txt"))

        logging.config.dictConfig(
            {
                'version': 1,
                'disable_existing_loggers': True,
                'formatters': {
                    'standard': {
                        'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                    },
                    'precise': {
                        'format': '%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s'
                    }
                },
                'handlers': {
                    'console': {
                        'level': console_level,
                        'formatter': 'standard',
                        'class': 'logging.StreamHandler',
                        'stream': 'ext://sys.stdout',
                    },
                    'file': {
                        'level': file_level,
                        'formatter': 'precise',
                        'class': 'logging.handlers.RotatingFileHandler',
                        'filename': log_file_name,
                        'maxBytes': file_max_bytes,
                        'backupCount': file_backup_count
                    }
                },
                'loggers': {
                    '': {
                        'handlers': ['console', 'file'],
                        'level': 'DEBUG',
                        'propagate': True
                    }
                }
            }
        )

    except (OSError, ValueError, TypeError):
        logging.basicConfig(level=logging.INFO)
        logging.exception("Could not configure the logging")


def main():
    """The function to launch the C2 Treatment nonmaleficence valuator component."""

    configure_log()
    app = App()
    app.start()
    app.stop()


if __name__ == "__main__":
    main()
