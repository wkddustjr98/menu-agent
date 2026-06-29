from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from ai.recommender import Recommender


app = FastAPI(title="SK hynix Menu Agent")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")

recommender = Recommender()


class RecommendRequest(BaseModel):
    message: str
    menus: list
    history: list = []


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "chat.html"
    )


@app.post("/api/recommend")
async def recommend(req: RecommendRequest):

    try:
        history = req.history or []

        answer = recommender.chat(
            user_message=req.message,
            menus=req.menus,
            history=history
        )

        return {
            "success": True,
            "data": {
                "type": "recommend",
                "recommendation": answer,
                "history": history
            }
        }

    except Exception as e:

        import traceback
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": str(e)
            }
        )


@app.get("/health")
async def health():
    return {"status": "ok"}