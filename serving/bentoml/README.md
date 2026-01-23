# BentoML Scaffolding

This folder is a placeholder for a BentoML-based model worker.

## Suggested structure

- `service.py`: BentoML service definition
- `requirements.txt`: dependencies (bentoml, torch, transformers, etc.)
- `bentofile.yaml`: build configuration

## Next step

`service.py` now provides a minimal BentoML mock service. Next:

- add `requirements.txt` and `bentofile.yaml`
- containerize and deploy as a worker if needed

## Files added

- `requirements.txt`
- `bentofile.yaml`
