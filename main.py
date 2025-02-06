from fastapi import FastAPI, Query, HTTPException
import requests

app = FastAPI()

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d**power for d in digits) == n

def get_fun_fact(n: int) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json", timeout=5)
        response.raise_for_status()
        return response.json().get("text", "No fun fact found.")
    except requests.RequestException:
        return "No fun fact found."


@app.get("/")
def read_root():
    return {"message": "API is Live!"}



@app.get("/api/classify_number")
def classify_number(number: int = Query(..., description="The number to classify")):
    properties = []
    
    if is_armstrong(number):
        properties.append("armstrong")
    
    properties.append("odd" if number % 2 else "even")

    return {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": sum(map(int, str(number))),
        "fun_fact": get_fun_fact(number)
    }
