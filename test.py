import os
import pprint
import utlis.jbf.toml as toml
import utlis.jbf.file as file
import logging
from digitalart import Session

logging.basicConfig(
    format="%(asctime)s %(levelname)s : %(name)s : %(lineno)d : %(message)s",
    datefmt="%Y%m%d_%H%M%S",
    level=logging.DEBUG,
    # file='sample.log',
)

log = logging.getLogger(__name__)


pp = pprint.PrettyPrinter(indent=4)


def main():
    # config
    cfg = toml.load_file("config.toml")
    cfg["ai"]["system_msg_file"] = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "system_msg.txt"
    )
    

    S = Session(cfg["input"]["folder"], cfg)
    S.get_fooocus()
    S.get_ai_description()


if __name__ == "__main__":
    main()
