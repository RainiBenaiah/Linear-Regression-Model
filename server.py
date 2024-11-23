import uvicorn
from main import app
import os
if __name__ == "__main__":
    # Get the port from the environment variable or use 8000 as default
    port = int(os.environ.get("PORT", 8000))
    # Run the FastAPI application using uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)

    
