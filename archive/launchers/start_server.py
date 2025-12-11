"""
Start Clisonix Cloud Industrial Backend
Author: Ledjan Ahmati
License: Closed Source
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "apps.api.master:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
