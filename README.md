# Telemetry DB Writer

A service running a django menegment command to write data to a database with batching and celery worker queue

reads telemetry clean and writes to its own time-seried postesql db

## Quick Start

example env is located in root repo as per convention in db-writer.env.example

```bash
docker compose up -d --build
```



## Testing

```bash
pytest
```

or from docker compose
```bash
docker compose exec db-web pytest
```
