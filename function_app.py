import json
from typing import Any

import azure.functions as func
from azure.functions import WsgiMiddleware

from stackability.app import app as flask_app
from stackability.app import SKU_TRAILER_CATALOG
import stackability.datatypes as dt
from stackability.stacker import Stacker

DOCS_HTML = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Stacking API Documentation</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
            margin: 0;
            background: #f7f7f7;
            color: #222;
        }

        .container {
            max-width: 900px;
            margin: 40px auto;
            background: white;
            padding: 32px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        }

        h1, h2, h3 {
            margin-top: 24px;
        }

        h1 {
            margin-top: 0;
            color: #c4001a;
        }

        code, pre {
            background: #111;
            color: #eee;
            padding: 10px;
            border-radius: 8px;
            display: block;
            overflow-x: auto;
            font-size: 13px;
        }

        inline-code {
            background: #eee;
            padding: 2px 6px;
            border-radius: 4px;
        }

        table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 10px;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }

        th {
            background: #fafafa;
        }

        .badge {
            display: inline-block;
            background: #ffe5e5;
            color: #c4001a;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: bold;
        }
    </style>
</head>

<body>
<div class="container">

<h1>Stacking API</h1>

<p class="badge">POST /api/stack</p>

<h2>Purpose</h2>
<p>
Checks whether a set of trailers can be stacked onto a valid lorry configuration.
If no full solution exists, the API returns the best partial stacking options.
</p>

<h2>Request</h2>

<pre>{
  "trailers": [
    {"sku": "1.00.1.0101.00", "quantity": 2},
    {"sku": "1.10.1.0807.05", "quantity": 1}
  ]
}</pre>

<h3>Fields</h3>

<table>
<tr><th>Field</th><th>Type</th><th>Required</th><th>Description</th></tr>
<tr><td>trailers</td><td>array</td><td>yes</td><td>List of trailer order lines</td></tr>
<tr><td>trailers[].sku</td><td>string</td><td>yes</td><td>Trailer SKU</td></tr>
<tr><td>trailers[].quantity</td><td>integer</td><td>no</td><td>Defaults to 1</td></tr>
</table>

<h2>Response (Complete Solution)</h2>

<pre>{
  "ok": true,
  "stackable": true,
  "solution_count": 1,
  "solutions": [
    {
      "stacks": [
        {
          "trailers": [
            {
              "sku": "1.00.1.0101.00-1",
              "model_name": "BSX 750.205x120",
              "length": 205,
              "width": 120,
              "height": 35,
              "axles": 1,
              "contained_trailer": null
            }
          ]
        }
      ]
    }
  ]
}</pre>

<h2>Response (Partial Solution)</h2>

<pre>{
  "ok": true,
  "stackable": false,
  "message": "No complete valid combination found",
  "partial_results": [
    {
      "placed_count": 3,
      "unplaced_count": 1,
      "filled_positions": 2,
      "total_positions": 4,
      "stacks": [...],
      "unplaced_trailers": [...]
    }
  ]
}</pre>

<h2>Trailer Object</h2>

<pre>{
  "sku": "1.10.1.0807.05",
  "model_name": "GTT 2500.301x151 VT3",
  "length": 301,
  "width": 151,
  "height": 153,
  "axles": 2,
  "contained_trailer": {
    "sku": "1.10.1.0101.02",
    "model_name": "GT 500.151x101 HT",
    ...
  }
}</pre>

<p>
<strong>Note:</strong> <code>contained_trailer</code> is used when a trailer is transported inside another trailer.
</p>

<h2>Error Responses</h2>

<h3>400 – Invalid JSON</h3>
<pre>{ "ok": false, "error": "Invalid JSON POST data" }</pre>

<h3>422 – Validation Error</h3>
<pre>{ "ok": false, "error": "Trailer 1 does not have a SKU" }</pre>

<h3>404 – SKU Not Found</h3>
<pre>{ "ok": false, "error": "Trailer with SKU ... not found" }</pre>

<h3>500 – Server Error</h3>
<pre>{ "ok": false, "error": "Unexpected error" }</pre>

<h2>Example</h2>

<pre>curl -X POST "https://.../api/stack" \
-H "Content-Type: application/json" \
-d '{
  "trailers": [
    {"sku": "1.00.1.0101.00", "quantity": 2}
  ]
}'</pre>

<h2>Notes</h2>
<ul>
<li>Only known SKUs are accepted</li>
<li>Invalid or incomplete trailer data is rejected</li>
<li>Max 5 full solutions are returned</li>
<li>If no full solution exists, up to 3 partial solutions are returned</li>
</ul>

</div>
</body>
</html>
"""


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

@app.route(route="docs", methods=["GET"])
def docs(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        body=DOCS_HTML,
        status_code=200,
        mimetype="text/html",
    )

@app.route(route="app/{*route}", methods=["GET", "POST"])
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return WsgiMiddleware(flask_app.wsgi_app).handle(req, context)