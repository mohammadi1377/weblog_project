from fastapi import FastAPI
from .router import post, root
from .DataBase.my_database import Base, engine


Base.metadata.create_all(bind=engine)
title = "Blog FastAPI"
description = f"""
{title} helps you do awesome stuff. 🚀
## Blogs
You will be able to:
* **Create blogs**.
* **Read all blogs**.
* **Delete own blogs**.
* **Vote blogs**.
## Users
You will be able to:
* **Create users**.
* **Login users**.
"""
app = FastAPI(
    title=title,
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "TEST",
        "url": "https://maktabsharif.ir/",
        "email": "mohammadbagherrezanejad@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)


app.include_router(post.router)
app.include_router(root.router)
