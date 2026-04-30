import json
from typing import Any

import azure.functions as func
from azure.functions import WsgiMiddleware

from stackability.app import app as flask_app
from stackability.app import SKU_TRAILER_CATALOG
import stackability.datatypes as dt
from stackability.stacker import Stacker


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


def json_response(payload: dict[str, Any], status_code: int = 200) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(payload, ensure_ascii=False),
        status_code=status_code,
        mimetype="application/json",
    )


def serialize_trailer(trailer: dt.Trailer) -> dict[str, Any]:
    contained = getattr(trailer, "contained_trailer", None)

    return {
        "sku": trailer.sku,
        "model_name": trailer.model_name,
        "length": trailer.length,
        "width": trailer.width,
        "height": trailer.height,
        "axles": trailer.axles,
        "contained_trailer": serialize_trailer(contained) if contained is not None else None,
    }


def serialize_stack(stack: dt.Stack) -> dict[str, Any]:
    return {
        "trailers": [
            serialize_trailer(trailer)
            for trailer in stack.trailers
        ],
    }


def build_trailers_from_api(payload: dict[str, Any]) -> list[dt.Trailer]:
    raw_trailers = payload.get("trailers", [])

    if not isinstance(raw_trailers, list) or len(raw_trailers) == 0:
        raise ValueError("Order does not contain trailers")

    trailer_objs: list[dt.Trailer] = []

    for idx, raw_trailer in enumerate(raw_trailers, start=1):
        if not isinstance(raw_trailer, dict):
            raise ValueError(f"Trailer {idx} must be an object")

        sku = raw_trailer.get("sku")
        if not sku:
            raise ValueError(f"Trailer {idx} does not have a SKU")

        quantity = int(raw_trailer.get("quantity", 1))
        if quantity < 1:
            raise ValueError(f"Trailer {idx} quantity must be at least 1")

        trailer_dct = SKU_TRAILER_CATALOG.get(str(sku))
        if trailer_dct is None:
            raise KeyError(f"Trailer with SKU {sku} not found")

        missing_fields = [
            field
            for field in ["height", "width", "length", "axles", "model_name"]
            if trailer_dct.get(field) is None
        ]

        if missing_fields:
            raise ValueError(
                f"SKU {sku} is not stackable because these fields are missing: {missing_fields}"
            )

        for copy_idx in range(quantity):
            trailer_objs.append(
                dt.Trailer(
                    sku=f"{sku}-{copy_idx + 1}" if quantity > 1 else str(sku),
                    height=int(trailer_dct["height"]),
                    width=int(trailer_dct["width"]),
                    length=int(trailer_dct["length"]),
                    axles=int(trailer_dct["axles"]),
                    model_name=str(trailer_dct["model_name"]),
                )
            )

    return trailer_objs


@app.route(route="stack", methods=["POST"])
def stack_input(req: func.HttpRequest) -> func.HttpResponse:
    try:
        json_data = req.get_json()
    except ValueError:
        return json_response({"ok": False, "error": "Invalid JSON POST data"}, 400)

    try:
        trailer_objs = build_trailers_from_api(json_data)
        stacker = Stacker(trailer_objs)

        results = stacker.stack_all(trailer_objs, max_results=5)

        if not results:
            partial_results = stacker.stack_partial(trailer_objs, max_results=3)

            return json_response(
                {
                    "ok": True,
                    "stackable": False,
                    "message": "No complete valid combination found",
                    "partial_results": [
                        {
                            "placed_count": result["placed_count"],
                            "unplaced_count": len(result["unplaced_trailers"]),
                            "filled_positions": result["filled_positions"],
                            "total_positions": result["total_positions"],
                            "stacks": [
                                serialize_stack(stack)
                                for stack in result["stacks"]
                            ],
                            "unplaced_trailers": [
                                serialize_trailer(trailer)
                                for trailer in result["unplaced_trailers"]
                            ],
                        }
                        for result in partial_results
                    ],
                },
                200,
            )

        return json_response(
            {
                "ok": True,
                "stackable": True,
                "solution_count": len(results),
                "solutions": [
                    {
                        "stacks": [
                            serialize_stack(stack)
                            for stack in solution
                        ],
                    }
                    for solution in results
                ],
            },
            200,
        )

    except KeyError as exc:
        return json_response({"ok": False, "error": str(exc)}, 404)

    except ValueError as exc:
        return json_response({"ok": False, "error": str(exc)}, 422)

    except Exception as exc:
        return json_response({"ok": False, "error": str(exc)}, 500)


@app.route(route="{*route}", methods=["GET", "POST"])
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return WsgiMiddleware(flask_app.wsgi_app).handle(req, context)