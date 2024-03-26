import os
import pprint
import utlis.jbf.toml as toml
import utlis.jbf.tools as tools
import logging as log
from digitalart import Session

log.basicConfig(
    format="%(asctime)s %(levelname)s : %(name)s : %(lineno)d : %(message)s",
    datefmt="%Y%m%d_%H%M%S",
    level=log.INFO,
    # file='sample.log',
)

pp = pprint.PrettyPrinter(indent=4)


def main():
    # config
    cfg = toml.load_file("config.toml")
    S = Session(cfg["input"]["folder"], cfg)
    print(S)


if __name__ == "__main__":
    main()
