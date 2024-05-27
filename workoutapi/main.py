from fastapi import FastAPI

from workoutapi.routers import router

app = FastAPI(title='Workout API', debug=True)

app.include_router(router)