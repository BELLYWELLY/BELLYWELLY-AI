from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
	return { "message" : "BellyWelly" }


if __name__ == '__main__':
    import uvicorn
    
    app_str = 'main:app'
    uvicorn.run(app_str, host='localhost', port=8001, reload=True, workers=1)