# Endpoints REST — sample2

Entregable NADF (modo automático). Stack `sample2-calculator-dev`, región `sa-east-1`.

## URLs

| API | URL |
|-----|-----|
| Base | `https://dsd3zcakg5.execute-api.sa-east-1.amazonaws.com/dev` |
| POST /calculate | `https://dsd3zcakg5.execute-api.sa-east-1.amazonaws.com/dev/calculate` |
| GET /history | `https://dsd3zcakg5.execute-api.sa-east-1.amazonaws.com/dev/history` |
| GET /health | `https://dsd3zcakg5.execute-api.sa-east-1.amazonaws.com/dev/health` |

## Ejemplos de consumo

```bash
# REQ-001: sumar
curl -s -X POST "https://dsd3zcakg5.execute-api.sa-east-1.amazonaws.com/dev/calculate" -H "content-type: application/json" \
  -d '{"operation": "add", "left": 2, "right": 3}'

# REQ-001: división por cero (espera 400)
curl -s -X POST "https://dsd3zcakg5.execute-api.sa-east-1.amazonaws.com/dev/calculate" -H "content-type: application/json" \
  -d '{"operation": "divide", "left": 1, "right": 0}'

# REQ-002: historial
curl -s "https://dsd3zcakg5.execute-api.sa-east-1.amazonaws.com/dev/history"

# REQ-003: salud
curl -s "https://dsd3zcakg5.execute-api.sa-east-1.amazonaws.com/dev/health"
```

## Smoke tests

- [PASS] GET /health → HTTP 200
- [PASS] POST /calculate add → HTTP 200
- [PASS] POST /calculate div0 → HTTP 400
- [PASS] GET /history → HTTP 200
