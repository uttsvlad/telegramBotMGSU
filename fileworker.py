import json

def write_to_file(filename:str, messages, mode:str)->None:
        
    with open(filename, mode, encoding="utf-8-sig") as file:
        for message in messages:
            file.write(message)
    file.close()
        
def read_from_file(filename):
    result = ""
    with open(filename, "r", encoding="utf-8-sig") as file:
        for message in file:
            result += message
    file.close()
    return result

def write_to_json(filename:str, data:dict) -> None:
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def read_from_json(filename:str) -> dict:
    with open(filename) as json_file:
        data = json.load(json_file)
    return data