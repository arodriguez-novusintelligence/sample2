# sample2 — Calculadora serverless (NADF)

Repositorio de aplicación generado por el ciclo NADF (modo automático).

- **Intake**: `nadf/initiative.yml` + `nadf/requests/`
- **Deploy**: solo entorno `dev` (PROD prohibido)
- **Stack**: `sample2-calculator-dev` · región `sa-east-1`

## APIs

| REQ | Método | Path | Descripción |
|-----|--------|------|-------------|
| REQ-001 | POST | `/calculate` | Suma, resta, multiplica o divide dos operandos |
| REQ-002 | GET | `/history` | Historial de cálculos persistidos en DynamoDB |
| REQ-003 | GET | `/health` | Estado del servicio |

### POST /calculate

Body JSON:

```json
{
  "operation": "add",
  "left": 10,
  "right": 5
}
```

Operaciones válidas: `add`, `subtract`, `multiply`, `divide`.

Respuesta exitosa (`200`):

```json
{ "result": 15 }
```

Errores de entrada o división por cero responden `400`.

### GET /history

Respuesta (`200`):

```json
{
  "items": [],
  "count": 0
}
```

Sin variable de entorno `TABLE_NAME` (modo local) devuelve lista vacía.

### GET /health

Respuesta (`200`):

```json
{
  "status": "ok",
  "service": "sample2-calculator"
}
```

## Estructura

```
src/
  calculator.py   # POST /calculate, GET /health
  history.py      # GET /history
template.yml      # AWS SAM (HTTP API + DynamoDB + Lambdas)
tests/
  test_calculator.py
  test_history.py
```

## Requisitos

- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Python 3.12
- Credenciales AWS configuradas para la región `sa-east-1`

## Construir

```bash
sam build
```

## Ejecutar tests

```bash
python -m unittest discover -s tests -v
```

## Desplegar (solo dev)

```bash
sam deploy \
  --stack-name sample2-calculator-dev \
  --region sa-east-1 \
  --parameter-overrides Stage=dev \
  --capabilities CAPABILITY_IAM \
  --resolve-s3 \
  --no-confirm-changeset
```

Tras el deploy, los outputs del stack incluyen `ApiUrl`, `CalculateUrl`, `HistoryUrl` y `HealthUrl`.

## Invocación local (sin AWS)

```bash
sam local start-api
```

Ejemplo:

```bash
curl -X POST http://127.0.0.1:3000/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation":"add","left":2,"right":3}'

curl http://127.0.0.1:3000/health
curl http://127.0.0.1:3000/history
```
