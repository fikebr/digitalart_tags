import toml

# https://www.pythonforbeginners.com/basics/working-with-toml-files-in-python


# def load_file(file):
#     """read a toml string from a file and return a python object"""
#     with open(file, 'rb') as f:
#         cfg = toml.loads(f.read().decode('utf-8'))

#     return cfg


def load_file(toml_filename):
    try:
        with open(toml_filename, 'rb') as f:
            # Try decoding with UTF-8 first
            try:
                cfg = toml.loads(f.read().decode('utf-8'))
                return cfg
            except UnicodeDecodeError:
                pass  # Move on to trying other encodings

            # Attempt with different encodings
            encodings = ['latin-1', 'cp1252']  # You can add more encodings here
            for encoding in encodings:
                try:
                    f.seek(0)  # Reset the file pointer
                    cfg = toml.loads(f.read().decode(encoding))
                    return cfg
                except UnicodeDecodeError:
                    pass  # Continue trying other encodings

            # If all encodings fail, return None
            print(f"Error: Could not decode file '{toml_filename}' with any supported encoding.")
            return None
    except FileNotFoundError:
        print(f"Error: File '{toml_filename}' not found.")
        return None

# Example usage
# parsed_data = parse_toml_with_error_handling("your_file.toml")



def save_file(tomlfile, data):
    """turn a python object into a toml string and save it to a file"""
    file = open(tomlfile, "w")
    toml.dump(data, file)
    file.close()


def to_toml(obj):
    """turn a python object into a toml string"""
    toml_string = toml.dumps(obj)
    return toml_string


def toml_parse(str):
    """turn a toml string into a python object"""
    data = toml.loads(str)
    return data
