import os
import pprint
import utlis.jbf.toml as toml
import utlis.jbf.tools as tools

pp = pprint.PrettyPrinter(indent=4)


def main():
    pid = 24452
    memory_usage_mb = tools.get_memory_usage(pid)
    print(f"Process (PID {pid}) memory usage: {memory_usage_mb:.2f} MB")

if __name__ == "__main__":
    main()
