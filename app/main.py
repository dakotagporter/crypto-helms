# Std Library Imports

# Third-party Imports
import uvicorn
from fastapi import FastAPI


# Instantiate app and app metadata
app = FastAPI(
    title: "Wine Helms",
    description: "Production web application for wine quality predictions.",
    version: "0.1"
)

# Endpoints
@app.get("/")
async def root():
    return {"message": "Hello, World!"}

if __name__ == '__main__':
    uvicorn.run(app)