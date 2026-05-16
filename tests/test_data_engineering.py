# ruff: noqa
import pytest

# Importamos las constantes desde tu módulo de utilidades
from data_engineering.utils.utils import WHITELIST_COLUMNS, IMPUTATION_COLUMNS


@pytest.mark.ci_exclude
def test_utils_constants_are_not_empty():
    """Verifica que las listas de configuración de columnas se importen correctamente."""
    # Comprobamos que existan y sean listas/diccionarios con datos
    assert WHITELIST_COLUMNS is not None
    assert len(WHITELIST_COLUMNS) > 0
    assert isinstance(IMPUTATION_COLUMNS, dict)


def test_ejemplo_simple():
    """Una prueba matemática básica para asegurar que pytest responda."""
    resultado = 1 + 1
    assert resultado == 2
