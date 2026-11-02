# Intent Boundary

Calibrate an abstention threshold for a local support assistant using labeled in-domain and out-of-domain queries. Evaluate the frozen threshold on a separate split.

## Run locally

Use Python 3.12. The project uses the standard library. From the repository root:

```sh
python cli.py example.json
python -m unittest -v
```

The included example is synthetic. Pass a different UTF-8 JSON file to inspect your own input. The command prints JSON to stdout. Invalid input returns status 2 and an explanation on stderr. See [CONTRACT.md](CONTRACT.md) for input fields and interpretation.

## Operational limits

A lexical nearest-neighbor model. Vocabulary overlap cannot establish semantic intent. Small synthetic fixtures demonstrate calibration and leakage detection; deployment requires representative labeled queries.

## Resumen en español

Calibra el umbral de un clasificador local y mide aceptaciones indebidas con consultas reservadas exclusivamente para evaluación.
