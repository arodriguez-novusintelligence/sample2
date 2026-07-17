# sample2 — Calculadora serverless (NADF)

Repositorio de aplicación generado por el ciclo NADF (modo automático).

- **Intake**: `nadf/initiative.yml` + `nadf/requests/`
- **Código**: generado por Cloud Agent (no incluir Lambdas en el seed)
- **Deploy**: solo entorno `dev` (PROD prohibido)
- **Stack**: `sample2-calculator-dev` · región `sa-east-1`

## APIs esperadas

| REQ | Método | Path |
|-----|--------|------|
| REQ-001 | POST | `/calculate` |
| REQ-002 | GET | `/history` |
| REQ-003 | GET | `/health` |
