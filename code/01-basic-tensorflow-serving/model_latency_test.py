import requests

# Send few actual requests and time average latency.                                                                                                                                                                   
total_time = 0
num_requests = 10
predict_request = '{"instances": [{ "input_number" : [10.0] },{ "input_number" : [20.0] }]}'
SERVER_URL = "http://localhost:8501/v1/models/test:predict"

for _ in range(num_requests):
    response = requests.post(SERVER_URL, data=predict_request)
response.raise_for_status()
total_time += response.elapsed.total_seconds()
prediction = response.json()
print("predictions : {}".format(prediction))
print('avg latency: {} ms'.format((total_time*1000)/num_requests))