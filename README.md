# Telemetry DB Writer

A service running a django menegment command to write data to a database with batching and celery worker queue

reads telemetry clean and writes to its own time-seried postesql db

docker package version 0.3:
```
ghcr.io/iot-hub-alpha/db-writer:v0.3@sha256:a6025a49e79f9b886b7983836c4153c11e3641c0aec20b4f1e5474eae51637a2
```

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
