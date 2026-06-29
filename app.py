from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel

from services.menu_service import MenuService


app = FastAPI(
    title="SK hynix Menu Agent"
)

app.add_middleware(
    SessionMiddleware,
    secret_key="CHANGE_THIS_SECRET_KEY"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")

service = MenuService()


class ChatRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request,
        "chat.html"
    )


@app.post("/api/chat")
async def chat(req: ChatRequest, request: Request):

    try:

        result = await service.process(
            req.message,
            request.session
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        import traceback

        traceback.print_exc()      # ★ 터미널에 오류 전체 출력

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": str(e)
            }
        )


@app.get("/api/reset")
async def reset(request: Request):

    request.session.clear()

    return {
        "success": True
    }


@app.get("/health")
async def health():

    return {
        "status": "ok"
    }