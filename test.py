import os
import pprint
import utlis.jbf.toml as toml
# import utlis.jbf.file as file
import logging
import traceback
from digitalart import Session

logging.basicConfig(
    format="%(asctime)s %(levelname)s : %(name)s : %(lineno)d : %(message)s",
    datefmt="%Y%m%d_%H%M%S",
    level=logging.INFO,
    # file='sample.log',
)

log = logging.getLogger(__name__)


pp = pprint.PrettyPrinter(indent=4)


def main():

    try:
        # config
        cfg = toml.load_file("config.toml")
        cfg["ai"]["system_msg_file"] = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "system_msg.txt"
        )
        

        S = Session(cfg["input"]["folder"], cfg)
        S.get_fooocus()
        # S.get_ai_description()
        #S.upscale()
        #S.toml_write()
        #S.toml_clean_abandoned()
        # S.adobe_stock_csv()
        # S.adobe_stock_mark_posted()

    except Exception as e:
        log.error(f"Error occurred in {__name__}")
        log.error(traceback.format_exc(e.__traceback__))
        log.error(f"Exception: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
