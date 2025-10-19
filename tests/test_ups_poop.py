import ast
from pathlib import Path

import pytest


def load_se_mi_ho():
    module_path = Path(__file__).resolve().parent.parent / "ups_modul" / "poop" / "ups_poop.py"
    source = module_path.read_text(encoding="utf-8")
    module_ast = ast.parse(source, filename=str(module_path))

    for node in module_ast.body:
        if isinstance(node, ast.FunctionDef) and node.name == "se_mi_ho":
            func_module = ast.Module(body=[node], type_ignores=[])
            compiled = compile(ast.fix_missing_locations(func_module), str(module_path), "exec")
            namespace = {}
            exec(compiled, namespace)
            return namespace["se_mi_ho"]

    raise AttributeError("se_mi_ho not found in ups_poop module")


se_mi_ho = load_se_mi_ho()


def test_se_mi_ho_returns_hours_minutes_seconds():
    hours, minutes, seconds = se_mi_ho(3661)

    assert hours == 1
    assert minutes == 1
    assert seconds == 1


def test_se_mi_ho_preserves_fractional_seconds():
    hours, minutes, seconds = se_mi_ho(7325.5)

    assert hours == 2
    assert minutes == 2
    assert seconds == pytest.approx(5.5)
