"""
# main.py
# This module initializes the FastAPI application and defines the main entry point.
"""
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to the Weather App API!"}

def main():
    """
    Main function to run the FastAPI application.
    """
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
