import logging
import logging.handlers

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a SysLogHandler to send logs to syslog
    syslog_handler = logging.handlers.SysLogHandler(address=('syslog', 514))

    # Set the log level for the handler
    syslog_handler.setLevel(logging.DEBUG)

    # Create a formatter to format log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Set the formatter for the handler
    syslog_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(syslog_handler)

    return logger

logger = setup_logger()
