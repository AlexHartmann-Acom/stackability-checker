from __future__ import annotations

from typing import Any
import json

from flask import Flask, render_template_string, request, send_from_directory, url_for

from stackability.factories import sx
from stackability import datatypes as dt


app = Flask(__name__)


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("stackability/static", filename)


HTML = """
<!doctype html>
<html lang="de">
<head>
    <meta charset="utf-8">
    <title>Stapellogik Anhänger</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        :root {
            --anssems-red: #c4001a;
            --anssems-red-dark: #a80016;
            --bg: #f5f5f5;
            --text: #222;
            --muted: #666;
            --border: #e6e6e6;
        }

        body {
            font-family: Arial, sans-serif;
            background: var(--bg);
            margin: 0;
            padding: 24px;
            color: var(--text);
        }

        .container {
            max-width: 1250px;
            margin: 0 auto;
        }

        .header {
            display: flex;
            align-items: center;
            gap: 22px;
            margin-bottom: 24px;
        }

        .logo {
            height: 52px;
            display: block;
        }

        h1 {
            margin: 0;
            color: var(--anssems-red);
        }

        .subtitle {
            color: var(--muted);
            margin-top: 4px;
        }

        .card {
            background: white;
            border-radius: 14px;
            padding: 22px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.07);
            margin-bottom: 20px;
        }

        .trailer-row {
            display: grid;
            grid-template-columns: 1.4fr 1fr 1fr 1fr 1fr 130px auto;
            gap: 10px;
            align-items: end;
            margin-bottom: 12px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border);
        }

        label {
            display: block;
            font-size: 12px;
            font-weight: bold;
            color: #444;
            margin-bottom: 4px;
        }

        input {
            width: 100%;
            box-sizing: border-box;
            padding: 9px 10px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 14px;
        }

        button {
            border: 0;
            border-radius: 8px;
            padding: 10px 14px;
            font-weight: bold;
            cursor: pointer;
            white-space: nowrap;
        }

        .btn-primary {
            background: var(--anssems-red);
            color: white;
        }

        .btn-primary:hover {
            background: var(--anssems-red-dark);
        }

        .btn-secondary {
            background: #fff0f0;
            color: var(--anssems-red);
        }

        .btn-danger {
            background: #ffe5e5;
            color: var(--anssems-red);
        }

        .btn-muted {
            background: #f0f0f0;
            color: #555;
        }

        .actions,
        .solution-nav {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
            margin-top: 16px;
        }

        .quantity-control {
            display: grid;
            grid-template-columns: 36px 1fr 36px;
            gap: 6px;
        }

        .quantity-display {
            text-align: center;
            font-weight: bold;
            padding: 9px;
            background: #fafafa;
            border-radius: 8px;
            border: 1px solid #ddd;
        }

        .result-error {
            border-left: 6px solid var(--anssems-red);
            background: #fff5f5;
        }

        .hint {
            color: var(--muted);
            font-size: 13px;
            margin-bottom: 0;
        }

        .summary {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 8px;
        }

        .summary-pill {
            background: #fff0f0;
            color: var(--anssems-red);
            border-radius: 999px;
            padding: 7px 12px;
            font-size: 13px;
            font-weight: bold;
        }

        .solution-counter {
            font-weight: bold;
            color: #444;
        }

        .lorry-wrap {
            margin-top: 18px;
            overflow-x: auto;
            padding-bottom: 8px;
        }

        .lorry-scene {
            min-width: 900px;
            padding: 20px 10px 6px 10px;
        }

        .lorry-load-area {
            display: grid;
            gap: 14px;
            align-items: end;
            min-height: 390px;
            padding: 0 32px;
        }

        .lorry-position {
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            align-items: center;
            min-height: 360px;
            position: relative;
        }

        .position-label {
            font-size: 12px;
            color: #777;
            margin-bottom: 8px;
        }

        .stack-pile {
            width: 100%;
            display: flex;
            flex-direction: column-reverse;
            align-items: center;
            justify-content: flex-start;
        }

        .trailer-block {
            width: var(--box-width);
            height: var(--box-height);
            min-height: 34px;
            max-width: 100%;
            background: linear-gradient(180deg, #d5162e 0%, #b80018 100%);
            color: white;
            border: 2px solid #8f0013;
            border-radius: 8px 8px 5px 5px;
            box-shadow: 0 4px 9px rgba(0,0,0,0.18);
            margin-top: -1px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
            text-align: center;
            overflow: hidden;
        }

        .trailer-block::before,
        .trailer-block::after {
            content: "";
            position: absolute;
            bottom: 5px;
            width: 13px;
            height: 13px;
            border-radius: 50%;
            background: #333;
            border: 2px solid #111;
        }

        .trailer-block::before {
            left: 13px;
        }

        .trailer-block::after {
            right: 13px;
        }

        .trailer-model {
            font-size: 14px;
            font-weight: bold;
            line-height: 1.1;
        }

        .trailer-dims {
            margin-top: 3px;
            font-size: 11px;
            opacity: 0.95;
        }

        .flatbed {
            height: 34px;
            background: linear-gradient(180deg, #3a3a3a, #222);
            border-radius: 6px;
            margin: 0 22px;
            position: relative;
            box-shadow: 0 5px 14px rgba(0,0,0,0.25);
        }

        .flatbed::before {
            content: "";
            position: absolute;
            left: -28px;
            bottom: 0;
            width: 36px;
            height: 42px;
            background: #2c2c2c;
            border-radius: 8px 0 0 8px;
        }

        .wheel {
            position: absolute;
            bottom: -20px;
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: #111;
            border: 5px solid #444;
            box-sizing: border-box;
        }

        .wheel.w1 { left: 8%; }
        .wheel.w2 { left: 16%; }
        .wheel.w3 { right: 16%; }
        .wheel.w4 { right: 8%; }

        .lorry-caption {
            text-align: center;
            color: #555;
            margin-top: 28px;
            font-size: 13px;
        }

        @media (max-width: 950px) {
            body {
                padding: 16px;
            }

            .trailer-row {
                grid-template-columns: 1fr 1fr;
            }

            .header {
                flex-direction: column;
                align-items: flex-start;
            }

            .logo {
                height: 44px;
            }
        }
    </style>
</head>

<body>
<div class="container">

    <div class="header">
        <img src="{{ url_for('static_files', filename='anssems-logo.svg') }}" class="logo">
        <div>
            <h1>Anhänger-Stapelprüfung</h1>
            <div class="subtitle">Modelle eintragen, Stückzahlen anpassen und Stapelplan auf dem LKW-Tieflader visualisieren</div>
        </div>
    </div>

    <form method="post" class="card" id="stackForm">
        <div id="trailerRows"></div>

        <div class="actions">
            <button type="button" class="btn-secondary" onclick="addTrailer()">+ Modell hinzufügen</button>
            <button type="button" class="btn-muted" onclick="addExample()">Beispiel laden</button>
            <button type="button" class="btn-danger" onclick="clearTrailers()">Leeren</button>
            <button type="submit" class="btn-primary">Stapelplan berechnen</button>
        </div>

        <p class="hint">Maße bitte in cm eingeben. Die Visualisierung skaliert Länge und Höhe relativ zu den eingegebenen Anhängern.</p>

        <input type="hidden" name="trailers_json" id="trailersJson">
    </form>

    {% if error %}
        <div class="card result-error">
            <h2>Nicht stapelbar / Fehler</h2>
            <p>{{ error }}</p>
        </div>
    {% endif %}

    {% if stack_solutions %}
        <div class="card">
            <h2>Stapelplan auf LKW-Tieflader</h2>

            <div class="summary">
                <div class="summary-pill"><span id="stackCount">{{ stack_count }}</span> Stapelpositionen</div>
                <div class="summary-pill"><span id="trailerCount">{{ trailer_count }}</span> Anhänger</div>
                <div class="summary-pill">{{ solution_count }} mögliche Lösung{% if solution_count != 1 %}en{% endif %}</div>
            </div>

            {% if solution_count > 1 %}
                <div class="solution-nav">
                    <button type="button" class="btn-muted" onclick="previousSolution()">← Vorherige Lösung</button>
                    <span class="solution-counter" id="solutionCounter"></span>
                    <button type="button" class="btn-secondary" onclick="nextSolution()">Nächste Lösung →</button>
                </div>
            {% endif %}

            <div class="lorry-wrap">
                <div class="lorry-scene">
                    <div class="lorry-load-area" id="lorryLoadArea"></div>

                    <div class="flatbed">
                        <div class="wheel w1"></div>
                        <div class="wheel w2"></div>
                        <div class="wheel w3"></div>
                        <div class="wheel w4"></div>
                    </div>

                    <div class="lorry-caption">
                        Schematische Darstellung: Länge und Höhe der Boxen sind relativ skaliert, nicht maßstabsgetreu.
                    </div>
                </div>
            </div>
        </div>
    {% endif %}
</div>

<script>
let trailers = {{ trailers | tojson }};
let stackSolutions = {{ stack_solutions | tojson }};
let currentSolutionIndex = 0;

function escapeHtml(value) {
    return String(value ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
}

function renderTrailers() {
    const container = document.getElementById('trailerRows');

    container.innerHTML = trailers.map((t, i) => `
        <div class="trailer-row">
            <div>
                <label>Modellname</label>
                <input value="${escapeHtml(t.model_name || '')}" onchange="trailers[${i}].model_name=this.value">
            </div>

            <div>
                <label>Länge</label>
                <input type="number" value="${escapeHtml(t.length || '')}" onchange="trailers[${i}].length=this.value">
            </div>

            <div>
                <label>Höhe</label>
                <input type="number" value="${escapeHtml(t.height || '')}" onchange="trailers[${i}].height=this.value">
            </div>

            <div>
                <label>Breite</label>
                <input type="number" value="${escapeHtml(t.width || '')}" onchange="trailers[${i}].width=this.value">
            </div>

            <div>
                <label>Achsen</label>
                <input type="number" value="${escapeHtml(t.axles || 2)}" onchange="trailers[${i}].axles=this.value">
            </div>

            <div>
                <label>Stückzahl</label>
                <div class="quantity-control">
                    <button type="button" class="btn-muted" onclick="decreaseQuantity(${i})">−</button>
                    <div class="quantity-display">${t.quantity || 1}</div>
                    <button type="button" class="btn-muted" onclick="increaseQuantity(${i})">+</button>
                </div>
            </div>

            <button type="button" class="btn-danger" onclick="removeTrailer(${i})">Entfernen</button>
        </div>
    `).join('');

    document.getElementById('trailersJson').value = JSON.stringify(trailers);
}

function increaseQuantity(i) {
    trailers[i].quantity = Number(trailers[i].quantity || 1) + 1;
    renderTrailers();
}

function decreaseQuantity(i) {
    const q = Number(trailers[i].quantity || 1);

    if (q <= 1) {
        trailers.splice(i, 1);
    } else {
        trailers[i].quantity = q - 1;
    }

    if (trailers.length === 0) {
        addTrailer();
    } else {
        renderTrailers();
    }
}

function removeTrailer(i) {
    trailers.splice(i, 1);

    if (trailers.length === 0) {
        addTrailer();
    } else {
        renderTrailers();
    }
}

function addTrailer() {
    trailers.push({
        model_name: '',
        length: '',
        height: '',
        width: '',
        axles: 2,
        quantity: 1
    });

    renderTrailers();
}

function clearTrailers() {
    trailers = [];
    addTrailer();
}

function addExample() {
    trailers = [
        {model_name:'MSX', length:405, height:180, width:120, axles:2, quantity:2},
        {model_name:'BSX', length:251, height:150, width:130, axles:1, quantity:1},
        {model_name:'GT', length:205, height:120, width:120, axles:1, quantity:3}
    ];

    renderTrailers();
}

function renderCurrentSolution() {
    if (!stackSolutions || stackSolutions.length === 0) {
        return;
    }

    const solution = stackSolutions[currentSolutionIndex];
    const loadArea = document.getElementById('lorryLoadArea');

    loadArea.style.gridTemplateColumns = `repeat(${solution.length}, minmax(145px, 1fr))`;

    loadArea.innerHTML = solution.map((stack, stackIndex) => `
        <div class="lorry-position">
            <div class="position-label">Position ${stackIndex + 1}</div>

            <div class="stack-pile">
                ${stack.map(trailer => `
                    <div class="trailer-block"
                         style="--box-width: ${trailer.visual_width}%; --box-height: ${trailer.visual_height}px;">
                        <div class="trailer-model">${escapeHtml(trailer.model_name)}</div>
                        <div class="trailer-dims">
                            ${trailer.length} × ${trailer.width} × ${trailer.height} cm
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `).join('');

    const solutionCounter = document.getElementById('solutionCounter');
    if (solutionCounter) {
        solutionCounter.innerText = `Lösung ${currentSolutionIndex + 1} von ${stackSolutions.length}`;
    }

    const stackCount = document.getElementById('stackCount');
    if (stackCount) {
        stackCount.innerText = solution.length;
    }

    const trailerCount = document.getElementById('trailerCount');
    if (trailerCount) {
        trailerCount.innerText = solution.reduce((sum, stack) => sum + stack.length, 0);
    }
}

function previousSolution() {
    if (!stackSolutions || stackSolutions.length === 0) {
        return;
    }

    currentSolutionIndex =
        (currentSolutionIndex - 1 + stackSolutions.length) % stackSolutions.length;

    renderCurrentSolution();
}

function nextSolution() {
    if (!stackSolutions || stackSolutions.length === 0) {
        return;
    }

    currentSolutionIndex =
        (currentSolutionIndex + 1) % stackSolutions.length;

    renderCurrentSolution();
}

document.getElementById('stackForm').addEventListener('submit', () => {
    document.getElementById('trailersJson').value = JSON.stringify(trailers);
});

if (trailers.length === 0) {
    addTrailer();
} else {
    renderTrailers();
}

renderCurrentSolution();
</script>

</body>
</html>
"""


def parse_int(value: Any, field_name: str) -> int:
    if value is None or value == "":
        raise ValueError(f"{field_name} ist erforderlich")

    try:
        return int(value)
    except ValueError:
        raise ValueError(f"{field_name} muss eine ganze Zahl sein")


def build_trailers(raw_trailers: list[dict[str, Any]]) -> list[dt.Trailer]:
    trailers: list[dt.Trailer] = []
    sku_counter = 1

    for idx, raw in enumerate(raw_trailers, start=1):
        model_name = str(raw.get("model_name", "")).strip()

        if not model_name:
            raise ValueError(f"Anhänger {idx}: Modellname ist erforderlich")

        quantity = parse_int(raw.get("quantity", 1), f"Anhänger {idx}: Stückzahl")

        if quantity < 1:
            raise ValueError(f"Anhänger {idx}: Stückzahl muss mindestens 1 sein")

        width = parse_int(raw.get("width"), f"Anhänger {idx}: Breite")
        height = parse_int(raw.get("height"), f"Anhänger {idx}: Höhe")
        length = parse_int(raw.get("length"), f"Anhänger {idx}: Länge")
        axles = parse_int(raw.get("axles"), f"Anhänger {idx}: Achsen")

        for _ in range(quantity):
            trailers.append(
                dt.Trailer(
                    sku=f"trailer-{sku_counter}",
                    width=width,
                    height=height,
                    length=length,
                    axles=axles,
                    model_name=model_name,
                )
            )
            sku_counter += 1

    return trailers


def serialize_stack_result(stacks: list[dt.Stack]) -> list[list[dict[str, Any]]]:
    all_trailers = [trailer for stack in stacks for trailer in stack.trailers]

    max_length = max((trailer.length for trailer in all_trailers), default=1)
    max_height = max((trailer.height for trailer in all_trailers), default=1)

    serialized: list[list[dict[str, Any]]] = []

    for stack in stacks:
        serialized_stack = []

        for trailer in stack.trailers:
            visual_width = 58 + (trailer.length / max_length) * 42
            visual_height = 42 + (trailer.height / max_height) * 48

            serialized_stack.append(
                {
                    "sku": trailer.sku,
                    "model_name": trailer.model_name,
                    "length": trailer.length,
                    "height": trailer.height,
                    "width": trailer.width,
                    "axles": trailer.axles,
                    "visual_width": round(visual_width, 1),
                    "visual_height": round(visual_height, 1),
                }
            )

        serialized.append(serialized_stack)

    return serialized


def serialize_stack_solutions(
    solutions: list[list[dt.Stack]],
) -> list[list[list[dict[str, Any]]]]:
    return [
        serialize_stack_result(solution)
        for solution in solutions
    ]


@app.route("/", methods=["GET", "POST"])
def index():
    trailers_for_ui: list[dict[str, Any]] = []
    stack_solutions: list[list[list[dict[str, Any]]]] = []
    error = None
    stack_count = 0
    trailer_count = 0
    solution_count = 0

    if request.method == "POST":
        try:
            trailers_for_ui = json.loads(request.form.get("trailers_json", "[]"))
            trailers = build_trailers(trailers_for_ui)

            # You will implement this in sx.py.
            # Expected return shape:
            # [
            #     [Stack, Stack, Stack],
            #     [Stack, Stack, Stack],
            #     ...
            # ]
            results = sx.stack_all(trailers, max_results=25)

            if not results:
                error = "Für diese Anhänger wurde kein gültiger Stapelplan gefunden."
            else:
                stack_solutions = serialize_stack_solutions(results)
                solution_count = len(stack_solutions)
                stack_count = len(stack_solutions[0])
                trailer_count = sum(len(stack) for stack in stack_solutions[0])

        except Exception as exc:
            error = str(exc)

    return render_template_string(
        HTML,
        trailers=trailers_for_ui,
        stack_solutions=stack_solutions,
        error=error,
        stack_count=stack_count,
        trailer_count=trailer_count,
        solution_count=solution_count,
    )