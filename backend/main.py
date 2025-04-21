from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel
from typing import List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LibraryResult(BaseModel):
    library: str
    availableCopies: int
    ownedCopies: int
    estimatedWaitDays: int

class SearchResponse(BaseModel):
    results: List[LibraryResult]

@app.get("/api/search/{query}")
async def search_books(query: str) -> SearchResponse:
    libraries = [
        ("nypl", "https://thunder.api.overdrive.com/v2/libraries/nypl/media"),
        ("brooklyn", "https://thunder.api.overdrive.com/v2/libraries/brooklyn/media")
    ]
    
    results = []
    async with httpx.AsyncClient() as client:
        for library_name, url in libraries:
            try:
                params = {
                    "query": query,
                    "format": "ebook-kindle",
                    "page": 1,
                    "perPage": 20
                }
                logger.info(f"Making request to {url} with query: {query}")
                response = await client.get(url, params=params)
                response.raise_for_status()  # Raise an exception for bad status codes
                data = response.json()
                
                if data.get("items") and len(data["items"]) > 0:
                    first_item = data["items"][0]
                    result = LibraryResult(
                        library=library_name,
                        availableCopies=first_item.get("availableCopies", 0),
                        ownedCopies=first_item.get("ownedCopies", 0),
                        estimatedWaitDays=first_item.get("estimatedWaitDays", 0)
                    )
                    results.append(result)
                else:
                    logger.warning(f"No items found for {library_name} with query: {query}")
            except Exception as e:
                logger.error(f"Error querying {library_name}: {str(e)}")
                logger.error(f"Response content: {response.text if 'response' in locals() else 'No response'}")
    
    return SearchResponse(results=results) 