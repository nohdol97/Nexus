# BentoML Scaffolding

This folder is a placeholder for a BentoML-based model worker.

## Suggested structure

- `service.py`: BentoML service definition
- `requirements.txt`: dependencies (bentoml, torch, transformers, etc.)
- `bentofile.yaml`: build configuration

## Next step

Implement `service.py` with a minimal BentoML service and add it to K8s as a
separate worker when needed.
