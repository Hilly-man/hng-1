from fastapi import FastAPI, Query, HTTPException
import requests

app = FastAPI()

# External API URL for fetching fun facts
EXTERNAL_API_URL = "https://hng-1-34sn.onrender.com/api/classify-number?number={number}"

@app.get("/")
def read_root():
    """Root endpoint to show API usage instructions"""
    return {"message": "Welcome to the Number Classifier API! Use /api/classify-number?number=371"}

@app.get("/api/classify-number")
def classify_number(number: int = Query(..., description="The number to classify")):
    """
    API endpoint to classify a number and fetch its fun fact.
    Example: /api/classify-number?number=371
    """

    # Check if the number is a valid integer
    if not isinstance(number, int):
        raise HTTPException(status_code=400, detail="Invalid number format. Please provide an integer.")

    # Properties of the number
    properties = []
    
    # Check if the number is prime
    if is_prime(number):
        properties.append("prime")
    
    # Check if the number is perfect
    if is_perfect(number):
        properties.append("perfect")
    
    # Check if the number is Armstrong
    if is_armstrong(number):
        properties.append("armstrong")
    
    # Check if the number is odd or even
    properties.append("odd" if number % 2 != 0 else "even")
    
    # Calculate digit sum
    digit_sum = sum(int(digit) for digit in str(number))

    # Fetch fun fact from external API
    fun_fact = get_fun_fact(number)

    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }

def is_prime(n: int) -> bool:
    """Checks if a number is prime"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Checks if a number is a perfect number"""
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    """Checks if a number is an Armstrong (Narcissistic) number"""
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

def get_fun_fact(number: int) -> str:
    """Fetches a fun fact for the number from the external API"""
    try:
        response = requests.get(EXTERNAL_API_URL.format(number=number))
        if response.status_code == 200:
            data = response.json()
            return data.get("fun_fact", "No fun fact available.")
        else:
            return "Error fetching fun fact."
    except requests.exceptions.RequestException:
        return "Failed to connect to external API."