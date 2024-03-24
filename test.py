import os
import pprint

import utlis.jbf.toml as toml

pp = pprint.PrettyPrinter(indent=4)


def main():
    t1 = toml.load_file(os.path.abspath("test.toml"))
    pp.pprint(t1)
    print("--------------")

    t2 = toml.load_file(os.path.abspath("test2.toml"))
    pp.pprint(t2)
    print("--------------")

    t3 = {}
    t3.update(t1)
    t3.update(t2)
    t3["files"].update(t1["files"])
    # t3["files"].update(t2["files"])

    pp.pprint(t3)


if __name__ == "__main__":
    main()
