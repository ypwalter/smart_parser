import json

class OutputFormatter:
    def __init__(self):
        pass

    def is_json(self, myjson):
        try:
            json_object = json.loads(myjson)
        except:
            return False
        return True

    # use the chosen style to produce result
    def output(self, style, input1, input2):
        if style == "json":
            return self.list_to_json(input1, input2)
        elif style == "list":
            return self.json_to_list(input1, input2)
        elif style == "json_file":
            return self.json_to_file(input1, input2)
        elif style == "list_file":
            return self.json_to_file(input1, input2)

    # Convert JSON to list, or returned if not JSON
    def json_to_list(self, error_json, warning_json):
        if error_json == "" or error_json == []:
            return ""
        elif self.is_json(error_json) is False:
            return error_json
        else:
            return ",".join([x for x in error_json[1]['ERROR']])

    # Convert list to JSON, or returned if not list
    def list_to_json(self, error_list, warning_list):
        if error_list == "" or error_list == []:
            return ""
        elif self.is_json(error_list) is True:
            dictA = json.loads(error_list)
            dictB = json.loads(warning_list)
            return {key: value for (key, value) in (dictA.items() + dictB.items())}
        else:
            return json.loads('[{"ERROR":' + json.dumps(error_list) + '}, {"WARNING":' + json.dumps(warning_list) + '}]')

    def json_to_file(self, error_json, warning_json, output_file):
        pass

    def list_to_file(self, error_list, warning_list, output_file):
        pass

