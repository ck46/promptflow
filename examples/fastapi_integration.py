"""
Example of PromptFlow integration with FastAPI.
"""

import os
from typing import List, Dict, Optional, Any
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from promptflow.api import PromptFlow
from promptflow.core.types import PromptCategory, MessageRole, Message


# Initialize the PromptFlow API
flow = PromptFlow()

# FastAPI app
app = FastAPI(
    title="PromptFlow API",
    description="API for managing prompts with PromptFlow",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Models for the API
class PromptRequest(BaseModel):
    """Request model for creating a prompt."""
    name: str
    system_message: Optional[str] = None
    user_message: str
    metadata: Dict[str, Any] = {}


class PromptResponse(BaseModel):
    """Response model for a prompt."""
    name: str
    version: str
    messages: List[Dict[str, Any]]
    metadata: Dict[str, Any] = {}


class ListResponse(BaseModel):
    """Response model for listing prompts."""
    prompts: List[str]


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize the database on startup."""
    flow.init()


@app.on_event("shutdown")
async def shutdown_event():
    """Close the database on shutdown."""
    flow.close()


# Routes
@app.post("/prompts", response_model=PromptResponse)
async def create_prompt(prompt_req: PromptRequest):
    """Create a new prompt."""
    # Create a prompt builder
    builder = flow.create_prompt()

    # Add messages
    if prompt_req.system_message:
        builder.add_system(prompt_req.system_message)
    builder.add_user(prompt_req.user_message)

    # Build the prompt
    prompt = builder.build()

    # Update metadata
    if prompt_req.metadata:
        # Convert category if present
        if "category" in prompt_req.metadata:
            try:
                category_name = prompt_req.metadata["category"]
                prompt_req.metadata["category"] = PromptCategory(category_name)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid category: {category_name}"
                )

        prompt.update_metadata(**prompt_req.metadata)

    # Save the prompt
    version = flow.save_prompt(prompt_req.name, prompt)

    # Convert to response model
    messages = [m.dict() for m in prompt.messages]
    metadata = prompt.metadata.dict() if prompt.metadata else {}

    return PromptResponse(
        name=prompt_req.name,
        version=version,
        messages=messages,
        metadata=metadata
    )


@app.get("/prompts", response_model=ListResponse)
async def list_prompts(category: Optional[str] = None):
    """List all prompts."""
    # Convert category if provided
    category_enum = None
    if category:
        try:
            category_enum = PromptCategory(category)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid category: {category}"
            )

    # Get the list of prompts
    prompts = flow.list_prompts(category=category_enum)

    return ListResponse(prompts=prompts)


@app.get("/prompts/{name}", response_model=PromptResponse)
async def get_prompt(
    name: str,
    version: Optional[str] = None,
    use_active: bool = True
):
    """Get a prompt."""
    # Get the prompt
    if use_active:
        prompt = flow.get_active_prompt(name)
    else:
        prompt = flow.get_prompt(name, version)

    if not prompt:
        raise HTTPException(
            status_code=404,
            detail=f"Prompt not found: {name}"
        )

    # Convert to response model
    messages = [m.dict() for m in prompt.messages]
    metadata = prompt.metadata.dict() if prompt.metadata else {}
    version = prompt.metadata.version if prompt.metadata else "unknown"

    return PromptResponse(
        name=name,
        version=version,
        messages=messages,
        metadata=metadata
    )


@app.put("/prompts/{name}/active/{version}")
async def set_active(name: str, version: str):
    """Set a prompt version as active."""
    # Check if the prompt exists
    prompt = flow.get_prompt(name, version)
    if not prompt:
        raise HTTPException(
            status_code=404,
            detail=f"Prompt not found: {name} version {version}"
        )

    # Set as active
    flow.set_active(name, version)

    return {
        "status": "success",
        "message": f"Prompt {name} version {version} set as active"
    }


@app.put("/prompts/{name}/fallback/{version}/{fallback_for}")
async def set_fallback(name: str, version: str, fallback_for: str):
    """Set a prompt version as a fallback for another prompt."""
    # Check if the prompt exists
    prompt = flow.get_prompt(name, version)
    if not prompt:
        raise HTTPException(
            status_code=404,
            detail=f"Prompt not found: {name} version {version}"
        )

    # Check if the fallback_for prompt exists
    fallback_target = flow.get_prompt(fallback_for)
    if not fallback_target:
        raise HTTPException(
            status_code=404,
            detail=f"Target prompt not found: {fallback_for}"
        )

    # Set as fallback
    flow.set_fallback(name, version, fallback_for)

    return {
        "status": "success",
        "message": (
            f"Prompt {name} version {version} set as fallback for {fallback_for}"
        )
    }


@app.get("/versions/{name}", response_model=List[str])
async def list_versions(name: str):
    """List all versions of a prompt."""
    # Check if the prompt exists
    versions = flow.list_versions(name)
    if not versions:
        raise HTTPException(
            status_code=404,
            detail=f"Prompt not found: {name}"
        )

    return versions


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 