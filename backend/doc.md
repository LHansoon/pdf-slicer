# The backend ᕕ( ᐛ )ᕗ

### api description

#### /getresult
- Method: GET
- Get result based on the mission id passed in
- Example: http://localhost:8000/getresult?mission-id=<mission-id>
- Return: {"mission-status": <mission status: finished | running | failed>, "request-status": "success", "Message": "request good"}

#### /postrequest
- Method: POST
- post new request based on the json
- Example: json file template the same as the one in \worker
- Return: {"request-status": "success", "Message": "request good"}

#### /getmissionid
- Method: GET
- generate new mission id
- Example: http://localhost:8000/getmissionid
- Return: {"mission-id": <mission id>, "request-status": "success", "Message": "request good"}

### API failures

#### unknown error
- {"request-status": "fail", "Message": "Unknown error ¯\\\_(ツ)_/¯"}

#### other errors
- skip