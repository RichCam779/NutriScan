from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Ajustamos la importación para que funcione desde la carpeta 'app'
from app.routes.user_routes import router as user_router

app = FastAPI(title="NutriScan API")

# Configuramos los orígenes para permitir tu entorno local y el futuro despliegue
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "*"  # Permite todos los orígenes temporalmente para facilitar el testeo en Vercel
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rutas
app.include_router(user_router)

@app.get("/")
def home():
    return {
        "message": "NutriScan API está en línea",
        "docs": "/docs"
    }

# Vercel no ejecuta el bloque __main__, usa su propio servidor (uvicorn)
# pero lo dejamos para que sigas pudiendo ejecutarlo localmente.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)