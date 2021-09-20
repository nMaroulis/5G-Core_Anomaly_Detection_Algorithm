from requests import get,put,post,exceptions
import pandas as pd
import json

data_simulation_1 = pd.read_csv("ad_dataset.csv")
client_ip = ""
client_port = ""


for k in range(data_simulation_1.shape[0]):
    data = data_simulation_1.to_dict('records')[k]
    try:
        r = post(client_ip + ":" + client_port + "/measurements", json={'ran_meas': data},
                 headers={'Content-Type': 'application/json'})
        r.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xxx
    except (exceptions.ConnectionError, exceptions.Timeout):
        print('Host is currently down :( ')
        break
    except exceptions.HTTPError:
        print(r.status_code)
    else:
        print(json.loads(r.text))

