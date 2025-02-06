from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

# Function to check if a number is prime
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to check if a number is perfect
def is_perfect(n: int) -> bool:
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

# Function to check if a number is Armstrong
def is_armstrong(n: int) -> bool:
    digits = [int(digit) for digit in str(n)]
    return sum([digit**len(digits) for digit in digits]) == n

# Function to calculate the sum of digits
def digit_sum(n: int) -> int:
    return sum([int(digit) for digit in str(n)])

# Function to fetch fun fact from Numbers API
def get_fun_fact(n: int) -> str:
    response = requests.get(f"http://numbersapi.com/{n}")
    return response.text

# Main endpoint
@app.get("/api/classify-number")
async def classify_number(number: int):
    if isinstance(number, int):
        prime = is_prime(number)
        perfect = is_perfect(number)
        armstrong = is_armstrong(number)
        properties = []

        if armstrong:
            properties.append("armstrong")
        if number % 2 == 0:
            properties.append("even")
        else:
            properties.append("odd")
        
        fact = get_fun_fact(number)
        
        return {
            "number": number,
            "is_prime": prime,
            "is_perfect": perfect,
            "properties": properties,
            "digit_sum": digit_sum(number),
            "fun_fact": fact
        }

    return {"number": str(number), "error": True}
