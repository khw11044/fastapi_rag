from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

#  CORS 정책에 의해 요청이 거부되는 것을 막는다
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # FastAPI에 CORS 예외 URL을 등록하여 해결
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일들 (html, css 등)에 접근
app.mount("/static", StaticFiles(directory="static"), name="static")

# 루트 페이지에서는 static/index.html을 불러옴 
@app.get("/")
async def root():                                   # 비동기처리: 여러 사용자들이 한꺼번에 홈페이지에 들어오더라도 여러가지 작업을 한꺼번에 처리할 수 있게 해줌 
    return FileResponse('static/index.html')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

