import uvicorn
from main import app
import os

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
