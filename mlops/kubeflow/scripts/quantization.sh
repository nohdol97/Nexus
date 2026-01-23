#!/bin/sh
set -e

echo "[step] quantization"

QUANT_METHOD="${QUANT_METHOD:-none}"
echo "quant_method=$QUANT_METHOD" > /workspace/quantization.txt
