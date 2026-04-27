import azure.functions as func
from azure.functions import WsgiMiddleware

from stackability.app import app as flask_app

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="{*route}", methods=["GET", "POST"])
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return WsgiMiddleware(flask_app.wsgi_app).handle(req, context)