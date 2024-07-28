import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.database.db import get_db
from src.routes import contacts, search, auth, comments

app = FastAPI()

@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        if result.fetchone() is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

app.include_router(auth.router)
app.include_router(contacts.router)
app.include_router(search.search)
app.include_router(comments.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
