import toml

# https://www.pythonforbeginners.com/basics/working-with-toml-files-in-python

def load_file(file):
    """read a toml string from a file and return a python object"""

    cfg = toml.load(file)
    return(cfg)


def save_file(tomlfile, data):
    """turn a python object into a toml string and save it to a file"""
    file=open(tomlfile,"w")
    # data_dict={
    #     "employee": {
    #         "name": "John Doe",
    #         "age": 35
    #     },
    #     "job": {
    #         "title": "Software Engineer",
    #         "department": "IT",
    #         "years_of_experience": 10
    #     },
    #     "address": {
    #         "street": "123 Main St.",
    #         "city": "San Francisco",
    #         "state": "CA",
    #         "zip": 94102
    #     }
    # }
    toml.dump(data,file)
    file.close()

def to_toml(obj):
    """turn a python object into a toml string"""
    toml_string = toml.dumps(obj)
    return(toml_string)


def toml_parse(str):
    """turn a toml string into a python object"""
    data = toml.loads(str)
    return(data)