import logging
import time

APP_NAME = "cron_tester"

from sebi_lib.utils import LinuxRunnable

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s P%(process)d l%(lineno)d@%(module)s.%(funcName)s : %(message)s")

def main():
    logging.info(F"{APP_NAME} has started.")

    logging.info(F"1: Sleep for 20 seconds.")
    time.sleep(20)

    logging.info(F"2: Sleep for 20 seconds.")
    time.sleep(20)

    logging.info(F"3: Sleep for 20 seconds.")
    time.sleep(20)

    logging.info(F"4: Sleep for 20 seconds.")
    time.sleep(20)

    logging.info(F"5: Sleep for 20 seconds.")
    time.sleep(20)

    logging.info(F"{APP_NAME} has finished.")

if __name__ == '__main__':
    runnable = LinuxRunnable(APP_NAME)
    main()