from fastapi import FastAPI, HTTPException, Query
import requests
from typing import List

app = FastAPI()

NUMBERS_API_URL = "http://numbersapi.com/{number}/math?json"

# Helper function to check if the number is prime
def is_prime(number: int) -> bool:
    if number <= 1:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True

# Helper function to check if the number is perfect
def is_perfect(number: int) -> bool:
    divisors_sum = sum(i for i in range(1, number) if number % i == 0)
    return divisors_sum == number

# Helper function to check if the number is Armstrong
def is_armstrong(number: int) -> bool:
    digits = [int(digit) for digit in str(number)]
    return sum(digit ** len(digits) for digit in digits) == number

# Helper function to calculate the digit sum
def digit_sum(number: int) -> int:
    return sum(int(digit) for digit in str(number))


# External endpoint URL
EXTERNAL_API_URL = "https://hng-1-34sn.onrender.com/api/classify-number?number={number}"

def get_fun_fact(number: int) -> str:
    # Send GET request to the external API with the number
    response = requests.get(EXTERNAL_API_URL.format(number=number))

    if response.status_code == 200:
        # Assuming the external API returns the required fun fact directly
        fact_data = response.json()
        
        # Extract the fun fact from the response
        fun_fact = fact_data.get("fun_fact", "")
        
        if fun_fact:
            return fun_fact  # Return the fun fact from the external API
        else:
            raise HTTPException(status_code=500, detail="Fun fact not found in the external API response")
    else:
        raise HTTPException(status_code=500, detail="Error fetching fun fact from external API")



def get_fun_fact(number: int) -> str:
    response = requests.get(NUMBERS_API_URL.format(number=number))
    if response.status_code == 200:
        fact = response.json().get("text", "")

        # Check if the returned fact mentions "narcissistic" (which is another term for Armstrong numbers)
        if "narcissistic" in fact.lower():
            # If it's an Armstrong number, provide the detailed calculation
            digits = [int(digit) for digit in str(number)]
            calculation = " + ".join(f"{digit}^{len(digits)}" for digit in digits)
            return f"{number} is an Armstrong number because {calculation} = {number}"

        return fact  # If it's not narcissistic, return the original fact

    else:
        raise HTTPException(status_code=500, detail="Error fetching fun fact from Numbers API")
    

@app.get("/api/classify-number")
async def classify_number(number: str = Query(...)):
    # Validate if the number is an integer
    try:
        number = int(number)
    except ValueError:
        return {"number": number, "error": True}

    # Classify the number properties
    properties = []

    if is_armstrong(number):
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    # Prepare the response data
    response_data = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number),
    }

    return response_data
