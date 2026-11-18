"""concubench: benchmark de agentes agnóstico al harness y al modelo.

El benchmark nunca llama a un modelo. Prepara contenedores, entrega un prompt a
un adaptador y califica el estado final de /workspace con pruebas deterministas.
"""
import sys

if sys.version_info < (3, 11):  # tomllib
    sys.exit("concubench necesita Python >= 3.11 (usa tomllib).")

__version__ = "0.1.0"
