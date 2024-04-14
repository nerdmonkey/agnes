import sys

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from mangum import Mangum

from config.app import get_settings
from routes import health, users

sys.path.append(".")
settings = get_settings()


description = """
Spartan, often called "The swiss army knife for serverless development," is a tool for
simplifying serverless application creation on popular cloud providers. It generates
Python code, streamlines development, saves time, and ensures code consistency. 🚀
"""


tags_metadata = [
    {
        "name": "Users",
        "description": "Operations related to users, providing functionality through a RESTful API.",
    },
    {
        "name": "Health Check",
        "description": "A health check endpoint to verify the API's functional condition.",
    },
]


settings = get_settings()


if settings.APP_ENVIRONMENT == "dev":
    root_path = "/dev/"
elif settings.APP_ENVIRONMENT == "uat":
    root_path = "/uat/"
elif settings.APP_ENVIRONMENT == "prod":
    root_path = "/prod/"
else:
    root_path = "/"


app = FastAPI(
    title="Spartan",
    description=description,
    version="0.2.5",
    terms_of_service="N/A",
    contact={
        "name": "Sydel Palinlin",
        "url": "https://github.com/nerdmonkey",
        "email": "sydel.palinlin@gmail.com",
    },
    openapi_tags=tags_metadata,
    root_path=root_path,
    debug=settings.APP_DEBUG,
)


allowed_origins = settings.ALLOWED_ORIGINS


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health.route)
app.include_router(users.route)


templates = Jinja2Templates(directory="public")


@app.get("/", include_in_schema=False)
async def read_welcome(request: Request):
    """
    Endpoint for the welcome page.

    Args:
        request (Request): The incoming request.

    Returns:
        TemplateResponse: A Jinja2 template response for the welcome page.
    """
    return templates.TemplateResponse(
        "static/welcome.html", {"request": request, "root_path": app.root_path}
    )


handle = Mangum(app)
