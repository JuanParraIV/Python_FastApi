from fastapi import FastAPI
from routes import products,users, users_db
from routes.auth import basic_auth_users, jwt_auth
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routes
app.include_router(products.router)
app.include_router(users.router)
app.include_router(users_db.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth.router)

#Exponer Recursos Estaticos
app.mount(
    path='/static',
    app= StaticFiles(directory='static'),
    name='static',
)

# Url local: http://127.0.0.1:8000
@app.get("/")
async def root():
    return {"message": "hello world"}


# Url local: http://127.0.0.1:8000/url
@app.get("/url")
async def root():
    return {"message": "hello juan"}


# Inicia el server: uvicorn server:app --reload
# Detener el server: CTRL+C

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc
