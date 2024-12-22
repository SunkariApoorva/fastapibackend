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

    results = get_plan_by_sentence(data,query)
    if results:
        return {"success": True, "plans": results}
    else:
        return {"success": False, "message": "No plans found."}

def fetch_plans_by_company(data, company_name):
    return [item["plan"] for item in data if item["compania"] == company_name]

if __name__ == "__main__":
    # Start the server with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



def get_plan_by_sentence(data, sentence):
    # Split the sentence into words
    words = set(sentence.lower().split())
    output = []
    # Find the matching company and return the plan
    for item in data:
        if item["compania"].lower() in words:
            output.append (item["plan"])
    return output

# Example usage
sentence = "Cuales son los productos de salud en ancon"
