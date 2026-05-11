# ETL - Extract, Transform, Load

## Visão Geral

Este projeto implementa um processo **ETL** (Extract, Transform, Load) para obter e processar dados da [API aberta da Câmara dos Deputados](https://dadosabertos.camara.leg.br/api/v2).

## O que é ETL?

| Etapa         | Descrição |
|---------------|-----------|
| **Extract**   | Extrair dados de uma fonte externa (API, banco de dados, etc.) |
| **Transform** | Transformar e validar os dados para o formato desejado |
| **Load**      | Carregar dados para um destino final (banco de dados, arquivo, etc.) |

## Fluxo do Processo

```
API Câmara → Extract → Transform → Validate → Load → Destino
```

## Arquivos do Módulo

### 📄 `extract.py`
Responsável pela extração de dados da API.
- Conecta à API https://dadosabertos.camara.leg.br/api/v2
- Implementa retry, timeout e tratamento de erros
- Obtém lista de deputados paginada
- Obtém detalhes de deputado específico

### 🔄 `transform.py`
Transforma dados brutos em formato útil.
- Normaliza estruturas de dados
- Limpa e valida campos
- Prepara dados para carga

### 💾 `load.py`
Carrega dados transformados para o destino final.
- Suporta banco de dados, CSV, JSON ou outros formatos

### ✅ `validators.py`
Valida integridade dos dados.
- Garante campos corretos antes do carregamento

### 📋 `logger_config.py`
Configura logs do sistema.
- `etl_logger`: execução do processo
- `api_logger`: chamadas à API

### 🚀 `main.py`
Ponto de entrada do projeto.
- Executa extração, transformação e carga em sequência

### 📦 `requirements.txt`
Dependências Python necessárias (ex: `requests`, etc.)
