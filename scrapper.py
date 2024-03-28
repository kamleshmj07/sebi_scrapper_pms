import yaml
from sebi_lib.models import Base 
from sebi_lib.sebi_parsing import *

from sebi_lib.utils import setup_file_logger
from sebi_lib.utils import LinuxRunnable
from sebi_lib.sebi_isin import scrap_sebi_isin

def main(yaml_config_path):    
    with open(yaml_config_path) as conf_file:
        config = yaml.load(conf_file, Loader=yaml.FullLoader)

    # runnable = LinuxRunnable(config['APP_NAME'])

    setup_file_logger(config['APP_NAME'], config['LOG_DIR'])
    logging.info(F"{config['APP_NAME']} has started.")

    url = mssql_prod_uri(True, "SEBI_PMS")

    if 'TABLE_CREATE' in config and config["TABLE_CREATE"]:
        create_tables(url, Base)

    db_session = get_database_scoped_session(url)
    # db_session = get_db_session(url, Base, True)

    # Scrap Sebi website for PMS Content
    scrap_whole_website(db_session, config["HTML_BACKUP"], False)
    # Check for missing data based on AMCScrapperStatus
    check_missing_data(db_session, config["HTML_BACKUP"], False)
    # check for ISIN status once a day (defined in the function)
    scrap_sebi_isin(db_session, False)

    logging.info(F"{config['APP_NAME']} has finished.")

if __name__ == '__main__':
    CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yaml')
    main(CONFIG_PATH)