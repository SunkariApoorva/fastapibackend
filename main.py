from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import uvicorn


app = FastAPI()

# Allow all origins for testing purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify a list of origins, like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/search_query")  # Define the API endpoint
async def search_query(payload: dict):
    query = payload.get("query", "").lower()
    with open("output.json", "r") as file:  # Assuming your JSON file is stored locally
        data = json.load(file)
    results = [entry['plan'] for entry in data if query in entry['company'].lower()]
    if results:
        return {"success": True, "plans": results}
    else:
        return {"success": False, "message": "No plans found."}

if __name__ == "__main__":
    # Start the server with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)