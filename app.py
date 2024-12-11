from fastapi import fastAPI, Query
import uvicorn
from db import index
from typing import List, Optional

app = fastAPI();
collection = index.collection 

@app.get("/filter_experts/")
async def filter_experts(
    panel: str,
    min_experience: int = Query(0, description="Minimum years of experience"),
    required_skills: Optional[List[str]] = Query(None, description="List of required skills"),
    language: Optional[str] = Query(None, description="Preferred language")
):
    # Build query dynamically
    query = {
        "specialization": {"$in": [panel]},
        "experience_years": {"$gte": min_experience},
    }

    if required_skills:
        query["skills"] = {"$all": required_skills}
    if language:
        query["languages"] = {"$in": [language]}

    # Query MongoDB
    experts = collection.find(query)
    results = [
        {"name": expert["name"], "qualification": expert["qualification"]}
        for expert in experts
    ]
    return {"matches": results}

experts = [
    {
        "name": "John Doe",
        "qualification": "Bachelor's in Naval Engineering",
        "experience_years": 15,
        "specialization": ["Naval Architecture", "Civil Engineering"],
        "languages": ["English", "German"],
        "skills": ["Dockyard Operations", "Project Management"]
    },
    {
        "name": "Jane Smith",
        "qualification": "Master's in Civil Engineering",
        "experience_years": 10,
        "specialization": ["Structural Engineering", "Civil Engineering"],
        "languages": ["English"],
        "skills": ["Project Management"]
    }
]

filter_experts(experts, panel="Naval Architecture", min_experience=13, required_skills=["Dockyard Operations"], language="German")
uvicorn.run(app, port=8000)