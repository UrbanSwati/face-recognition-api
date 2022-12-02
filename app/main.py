from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from app.routers import compare, load_image
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Face Regonation API",
    version="1.0.0",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_V1 = "/api/v1"

@app.get("/", response_class=HTMLResponse)
async def index_route(request: Request):
    html_content = f"""
    <!doctype html>
<html>
  <head>
    <title>Pokemon API!</title>
  </head>
  <body>
    <h3> For the Swagger API docs got to {request.base_url}docs <br/>thanks for using our service :) </h3>
  </body>
</html>
    """
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)


app.include_router(compare.router, prefix=API_V1, tags=["Compare"])
app.include_router(load_image.router, prefix=API_V1, tags=["Load Image"])