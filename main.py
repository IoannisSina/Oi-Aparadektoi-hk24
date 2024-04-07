import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import descriptor


# Create the FastAPI instance
app = FastAPI()

# Post url to get description
@app.post("/description")
async def get_description(url:str):
    response = descriptor.get_description(url)
    return response


# @app.post("/description")
# async def get_description(url:str):
#     response = get_description(url)
#     return response



# Starting the server function using uvicorn
def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
