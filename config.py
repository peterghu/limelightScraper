import pathlib
import configparser

parser = configparser.ConfigParser()
parser.read('config.ini')

CONFIG_PATH = pathlib.Path(__file__) / 'config.ini'
OUTPUT_PATH = parser.get('Folders', 'output')

ORGANIZATION_ID  = parser.get('Authorization', 'organization')
ACCESS_KEY       = parser.get('Authorization', 'accesskey')
SECRET_KEY       = parser.get('Authorization', 'secretkey')
KEY_EXPIRES      = parser.get('Authorization', 'keyExpiry')

PRINT_MEDIA_LIST = int(parser.get('Settings', 'printCatalogueToJson'))
DISABLE_DOWNLOAD = int(parser.get('Settings', 'disableDownload'))
DOWNLOAD_DELAY   = int(parser.get('Settings', 'downloadDelay'))
MAX_DOWNLOADS    = int(parser.get('Settings', 'maxDownloads'))
START_ITERATION  = int(parser.get('Settings', 'downloadStartPoint'))


