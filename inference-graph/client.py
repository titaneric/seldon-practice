import requests

resp = requests.post("http://localhost:5000/predict",
                     files={"binData": open('img/sample_file.jpeg','rb')})

print(resp.json())