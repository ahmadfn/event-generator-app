import os
import uuid
import json
from datetime import datetime

def repeat_input():
    order_numbers = int(input("order numbers: ").strip())
    batch_size = int(input("batch size: ").strip())

    return order_numbers, batch_size

def create_event(event_type):
    event = {
        "type": event_type,
        "data": {
            "order_id": str(uuid.uuid1()),
            "order_time": datetime.now().strftime("%y-%m-%d %H:%M:%S")
        }
    }

    return event

def create_order(type):
    submitted = create_event("order_submitted")

    if (type == "delivered"):
        result_event = create_event("order_delivered")
    else:
        result_event = create_event("order_cancelled")

    return submitted, result_event

def create_json(data, path):
    timestamp = datetime.now().strftime("%y%m%d%H%M%S%f")
    filename = f"order_collection-{timestamp}.json"

    with open(os.path.join(path, filename), "w") as write_file:
        json.dump(data, write_file, indent= 4)

try:
    order_numbers, batch_size = repeat_input()
    total_events = order_numbers * 2

    while total_events < batch_size:
        print("Total events must be equal or greater than batch size")
        print("Remember: order numbers is equal to two events")
        order_numbers, batch_size = repeat_input()

    s = input("output directory: ").strip()
    output_dir = s.replace(s[0], '', 1) if s[0] == '/' else s
    path = os.path.join(os.getcwd(), output_dir)
    isExisted = os.path.exists(path)
    
    if isExisted == False:
        os.makedirs(path)

    json_file = { "data": [] }

    i = 1
    # json_file_length = 2 if batch_size % 2 == 0 else 1
    # index_arr = []
    while i <= order_numbers:
        if (i % 5 == 0):
            event_submitted, result_event = create_order("cancelled")
        else:
            event_submitted, result_event = create_order("delivered")

        json_file["data"].append(event_submitted)
        json_file["data"].append(result_event)
        
        # if json_file_length == batch_size:
        #     create_json(json_file, path)
        #     index_arr.append(json_file_length)
        #     json_file_length -= batch_size
        # elif i == order_numbers:
        #     json_file2 = {"data": []}
        #     json_file2["data"].append(json_file["data"][index_arr[-1]:])
        #     create_json(json_file2, path)
        # else:
        #     if batch_size % 2 == 0:
        #         json_file_length += 2
        #     else:
        #         json_file_length += 1

        i += 1

    num_of_files = total_events / batch_size
    if total_events % batch_size != 0:
        num_of_files += 1

    start_index = 0
    last_index = batch_size
    data_length = len(json_file["data"])

    i = 1
    while i <= num_of_files:
        json_file2 = { "data": [] }
        json_file2["data"].append(json_file["data"][start_index:last_index])
        create_json(json_file2, path)

        print(f'start_index: {start_index}')
        print(f'last_index: {last_index}')

        start_index = last_index
        last_index += batch_size

        i += 1


except ValueError:
    print("Order numbers and batch size must be an integer")
    print("Program is exited")
except OSError:
    print("Creation of directory failed. Target directory already exists")
    print("Program is exited")
except IndexError:
    print("error")