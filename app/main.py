from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine

def create_tables():
    """Creates all database tables."""
    Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Fin-Watch: Multi-Currency FX Alerter",
    description="A backend microservice that provides real-time currency exchange data, executes conversions, and offers a user-defined alerting system.",
    version="1.0.0",
)

@app.on_event("startup")
def on_startup():
    # This will create the tables in the database on application startup.
    # In a production environment, you would typically use a migration tool like Alembic.
    print("Creating database tables...")
    create_tables()
    print("Database tables created.")


@app.get("/", tags=["Root"])
def read_root():
    """A welcome message to verify the service is running."""
    return {"message": "Welcome to the Fin-Watch API"}

# The API routers will be included here in a later step.
from app.api.endpoints import auth, users, rates, alerts
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(rates.router, prefix="/api", tags=["Rates & Conversion"])
app.include_router(alerts.router, prefix="/api", tags=["Alerts"])
