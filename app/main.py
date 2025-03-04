from fastapi import FastAPI
from routers.routes import router
import uvicorn  
from sevices.rule_based_detection import RuleBasedFraudMonitoringService
from config import config
import pandas as pd
app = FastAPI()

app.include_router(router)

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()