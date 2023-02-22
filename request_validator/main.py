import csv
import re
import json


def build_response(request, action, additional):
    response_fields = action.split('|')
    print(action)
    response_dict = {}
    for field in response_fields:
        key, value = field.split(':')
        response_dict[key] = value
    response = '|'.join(response_fields)
    response = response + "|" + request.replace("RequestType:NEWORDER|","") + "|" + additional
    # print(response + "|" + request)
    return response


def compare(x, operator, comparator, value):
    # print(str(x) + " | " + str(operator) + " | " + str(value))
    if comparator == "int":
        x = int(x)
    elif comparator == "float":
        x = float(x)
    else:
        x = str(x)
    if operator == "greaterthan":
        return x > value
    elif operator == "lessthan":
        return x < value
    elif operator == "equals":
        return x == value
    else:
        raise ValueError("Invalid operator: {}".format(operator))


def process_request(request):
    with open('request_validator/rules.json', 'r') as f:
        rules = json.load(f)
    fields = re.findall(r'(\w+):([\w\.]+)', request)

    request_dict = dict(fields)
    response = []
    # print(rules)

    for rule in rules:
        conditions = rule['conditions']
        action = rule['action']
        match = True
        additional = rule['additional_fields']
        # print("========")

        for item in conditions:
            # print(item)

            if "operator" in item:
                operator = item["operator"]
            if "comparator" in item:
                comparator = item["comparator"]
            for key, value in item.items():
                if key != "operator" and key != "comparator":
                    print(f"{key} {value} {action}")

                    result = compare(request_dict.get(key), operator, comparator, value)
                    if not result:
                        match = False
                        # print(f"{key} {value} - skip")
                        break

            if not match:
                break

        if match:
            if "REJECT" in action:
                return [build_response(request, action, additional)]
            response.append(build_response(request, action, additional))
    return response


if __name__ == '__main__':
    # Example request
    # request = 'RequestType:NEWORDER|OrderID:480069891|Token:0|Symbol:IFEU_BRN|Side:B|Price:150|Quantity:5|QuantityFilled:0|DisclosedQnty:5|TimeStamp:1666287639395048969|Duration:DAY|OrderType:LIMIT|Account:bJEROM|Exchange:0|NumCopies:0'
    with open('request_validator/inputs.csv', 'r') as file:
        reader = csv.reader(file)
        rows = [row for row in reader]
        # print(rows)


    with open('request_validator/inputs.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            result = process_request(row[0])
            # print (result)
            for item in result:
                row.append(item)
            writer.writerow(row)
            #