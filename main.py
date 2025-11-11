import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents

app = FastAPI(title="IT Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "IT Portfolio API running"}


# Schemas for runtime request validation (simple proxies to schemas.py)
class PortfolioProfileIn(BaseModel):
    full_name: str
    title: str
    bio: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None
    photo_base64: Optional[str] = None


class ProjectIn(BaseModel):
    title: str
    description: str
    tags: List[str] = []
    live_url: Optional[str] = None
    repo_url: Optional[str] = None
    image_base64: Optional[str] = None


@app.post("/api/profile")
def create_profile(payload: PortfolioProfileIn):
    try:
        from schemas import PortfolioProfile
        inserted_id = create_document("portfolioprofile", PortfolioProfile(**payload.model_dump()))
        return {"id": inserted_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/profile")
def get_profile():
    try:
        docs = get_documents("portfolioprofile", {}, limit=1)
        if not docs:
            return {"profile": None}
        # Convert ObjectId and datetime to strings for JSON
        doc = docs[0]
        doc["_id"] = str(doc.get("_id"))
        if "created_at" in doc:
            doc["created_at"] = str(doc["created_at"])
        if "updated_at" in doc:
            doc["updated_at"] = str(doc["updated_at"])
        return {"profile": doc}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/projects")
def create_project(payload: ProjectIn):
    try:
        from schemas import Project
        inserted_id = create_document("project", Project(**payload.model_dump()))
        return {"id": inserted_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/projects")
def list_projects():
    try:
        docs = get_documents("project")
        for d in docs:
            d["_id"] = str(d.get("_id"))
            if "created_at" in d:
                d["created_at"] = str(d["created_at"])
            if "updated_at" in d:
                d["updated_at"] = str(d["updated_at"])
        return {"projects": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
