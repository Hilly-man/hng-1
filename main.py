from fastapi import FastAPI, Query, HTTPException
import requests

app = FastAPI()

# Numbers API URL for fun facts
NUMBERS_API_URL = "http://numbersapi.com/{number}/math?json"

@app.get("/")
def read_root():
    """Root endpoint providing usage instructions."""
    return {"message": "Welcome to the Number Classifier API! Use /api/classify-number?number=371"}

@app.get("/api/classify-number")
def classify_number(number: str = Query(..., description="The number to classify")):
    """
    Classifies the given number based on mathematical properties.
    """

    # Validate that the input is an integer
    try:
        number = int(number)
    except ValueError:
        raise HTTPException(status_code=400, detail={"number": number, "error": True})

    # Classify number properties
    properties = []
    
    if is_prime(number):
        properties.append("prime")
    
    if is_perfect(number):
        properties.append("perfect")
    
    if is_armstrong(number):
        properties.append("armstrong")
    
    properties.append("odd" if number % 2 != 0 else "even")

    # Calculate digit sum
    digit_sum = sum(int(digit) for digit in str(number))

    # Fetch fun fact from the Numbers API
    fun_fact = get_fun_fact(number)

    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }

# Helper function to check if a number is prime
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Helper function to check if a number is perfect
def is_perfect(n: int) -> bool:
    return sum(i for i in range(1, n) if n % i == 0) == n

# Helper function to check if a number is an Armstrong (Narcissistic) number
def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

# Fetch fun fact from the Numbers API
def get_fun_fact(number: int) -> str:
    try:
        response = requests.get(NUMBERS_API_URL.format(number=number))
        if response.status_code == 200:
            data = response.json()
            return data.get("text", "No fun fact available.")
        return "Error fetching fun fact."
    except requests.exceptions.RequestException:
        return "Failed to connect to external API."
