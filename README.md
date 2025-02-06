 Number Classification API

 Overview
This is a FastAPI-based API that classifies a given number based on its mathematical properties and provides a fun fact using the Numbers API.

 Features
- Determines if a number is prime
- Checks if a number is perfect
- Identifies if a number is an Armstrong number
- Classifies the number as odd or even
- Calculates the sum of its digits
- Fetches a fun fact about the number
- Returns data in JSON format
- Handles CORS for cross-origin requests

 API Endpoint
 GET /api/classify-number
 Request Parameters
| Parameter | Type  | Required | Description |
|-----------|-------|----------|-------------|
| number    | int   | Yes      | The number to classify |

 Example Request
```sh
curl -X GET "https://your-api-url.onrender.com/api/classify-number?number=371"
```

 Success Response (200 OK)
```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
    
}
```

 Error Response (400 Bad Request)
```json
{
    "number": "alphabet",
    "error": true
}
```

 Installation & Running Locally

 1. Clone the Repository
```sh
git clone https://github.com/Hilly-man/hng-1.git
cd hng-1
```

 2. Create a Virtual Environment (Optional but recommended)
```sh
python -m venv venv
source venv/bin/activate   On Windows, use: venv\Scripts\activate
```

 3. Install Dependencies
```sh
pip install -r requirements.txt
```

 4. Run the Server
```sh
uvicorn main:app --reload
```
Server will start at: http://127.0.0.1:8000

 Deployment
This API is deployed on Render and publicly accessible at:
[https://your-api-url.onrender.com](https://your-api-url.onrender.com)

 Testing
Once running, you can test the API using:
- Curl:
  ```sh
  curl -X GET "http://127.0.0.1:8000/api/classify-number?number=371"
  ```
- Postman
- Open http://127.0.0.1:8000/docs to explore the API with Swagger UI.

 License
This project is open-source and available under the Hillytech License.

 Author
Hilkiah Edem

