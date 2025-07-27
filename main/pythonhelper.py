from help_commands.pythonhelper.register_all import *

register_dp()
tables = Tables(0, 0, None)


def lambda_handler():
    logger = logging.getLogger()
    logger.warning('Hello!')
    executor.start_polling(dp)


lambda_handler()
