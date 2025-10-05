from __future__ import annotations
from pathlib import Path
import csv
from typing import List, Dict, Optional

# Pure functions: safe to import in environments without FastAPI installed
def load_students(csv_path: Optional[str | Path] = None) -> List[Dict[str, object]]:
    """Load students from a CSV file and return a list of dicts in file order.

    Each row becomes {"studentId": int, "class": str}
    """
    path = Path(csv_path) if csv_path else Path(__file__).parent / "students.csv"
    students: List[Dict[str, object]] = []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            # Normalize keys and types
            sid = row.get("studentId")
            cls = row.get("class")
            try:
                sid_val = int(sid) if sid is not None and sid != "" else None
            except ValueError:
                sid_val = None
            students.append({"studentId": sid_val, "class": cls})
    return students


def filter_students(students: List[Dict[str, object]], classes: Optional[List[str]] = None) -> List[Dict[str, object]]:
    """Filter students by class list. If classes is None or empty, return all students.

    Preserve the original order of `students`.
    Comparison is exact (case-sensitive) to match CSV values.
    """
    if not classes:
        return students
    classes_set = set(classes)
    return [s for s in students if s.get("class") in classes_set]


# Try to wire FastAPI app if available. This block is safe to import even when FastAPI is not installed.
try:
    from fastapi import FastAPI, Query
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi import HTTPException
    FASTAPI_AVAILABLE = True
except Exception:
    FASTAPI_AVAILABLE = False


if FASTAPI_AVAILABLE:
    app = FastAPI()

    # Allow GET requests from any origin
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"])

    @app.get("/api")
    async def get_students(class_: Optional[List[str]] = Query(None, alias="class")):
        """Return students, optionally filtered by repeated `class` query params.

        Examples:
        /api -> all students
        /api?class=1A -> only class 1A
        /api?class=1A&class=1B -> 1A and 1B
        """
        students = load_students()
        result = filter_students(students, class_)
        return {"students": result}

    # Helpful health endpoint
    @app.get("/")
    async def root():
        return {"message": "FastAPI students API"}


if __name__ == "__main__":
    # Run with: python server.py (requires uvicorn installed or run via `uv run server.py`)
    try:
        import uvicorn
        uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)
    except Exception:
        print("uvicorn is not available. Install uvicorn or run with 'uv run server.py'")
