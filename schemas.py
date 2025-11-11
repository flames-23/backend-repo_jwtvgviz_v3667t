"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Portfolio schemas

class PortfolioProfile(BaseModel):
    """
    Portfolio profile details (singleton document)
    Collection name: "portfolioprofile"
    """
    full_name: str = Field(..., description="Your full name")
    title: str = Field(..., description="Professional title e.g., Flutter Developer")
    bio: Optional[str] = Field(None, description="Short bio/summary")
    linkedin: Optional[HttpUrl] = Field(None, description="LinkedIn profile URL")
    github: Optional[HttpUrl] = Field(None, description="GitHub profile URL")
    website: Optional[HttpUrl] = Field(None, description="Personal website or portfolio URL")
    photo_base64: Optional[str] = Field(None, description="Profile photo as Base64 data URL")

class Project(BaseModel):
    """
    IT project item for portfolio
    Collection name: "project"
    """
    title: str = Field(..., description="Project title")
    description: str = Field(..., description="What it is and your impact")
    tags: List[str] = Field(default_factory=list, description="Tech stack / keywords")
    live_url: Optional[HttpUrl] = Field(None, description="Live demo URL")
    repo_url: Optional[HttpUrl] = Field(None, description="Repository URL")
    image_base64: Optional[str] = Field(None, description="Screenshot as Base64 data URL")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
