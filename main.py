from typing import List, Optional
from pathlib import Path
import pandas as pd
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS to allow GET requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Prefer the provided q-fastapi.csv. Check common locations:
base = Path(__file__).parent
candidate_paths = [base / "q-fastapi.csv", base / "Q11" / "q-fastapi.csv"]
# Start with an empty dataframe so the app always has a DataFrame object
students_df = pd.DataFrame(columns=["studentId", "class"])
for p in candidate_paths:
    if p.exists():
        students_df = pd.read_csv(p)
        break


@app.get("/api")
def get_students(class_filter: Optional[List[str]] = Query(None, alias="class")):
    if not class_filter:
        filtered = students_df
    else:
        filtered = students_df[students_df["class"].isin(class_filter)]
    # Ensure studentId is the type expected (int) and preserve order
    result = filtered.to_dict("records")
    # Convert studentId to int if possible
    for r in result:
        try:
            r["studentId"] = int(r["studentId"])
        except Exception:
            pass
    return {"students": result}

@app.get("/")
def root():
    return {"message": "FastAPI students API"}
