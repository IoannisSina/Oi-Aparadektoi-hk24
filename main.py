import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import time
import descriptor


# Create the FastAPI instance
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Post url to get description
@app.get("/description/{url}")
async def get_description(url:str):
    # time.sleep(25)
    # response = f"This is a description for {url}"
    response = descriptor.get_description(url)
    return response


# @app.post("/description")
# async def get_description(url:str):
#     response = get_description(url)
#     return response



# Starting the server function using uvicorn
def start():
    uvicorn.run(app, host="0.0.0.0", port=8000)

start()
