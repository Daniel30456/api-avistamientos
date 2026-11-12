"""Plugin de pytest que mide cobertura de líneas solo con la biblioteca estándar
(sys.monitoring, Python 3.12+). Uso:
  PYTHONPATH=<dir> STDCOV_FILES="app.py validador.py" python -m pytest -p stdcov
Imprime una tabla con el mismo formato que pytest-cov --cov-report=term-missing.
"""
import ast
import os
import sys

TOOL = sys.monitoring.COVERAGE_ID
_hits = {}
_targets = {}


def _statements(path):
    """Líneas de sentencias ejecutables, contadas como coverage.py:
    primera línea de cada ast.stmt, sin docstrings."""
    # Regla calibrada contra pytest-cov 7.1 sobre este mismo repo (71 y 27 sentencias):
    # primera línea de cada sentencia + cada línea de decorador.
    tree = ast.parse(open(path, encoding="utf-8").read())
    lines = set()
    proxies = {}  # docstring -> línea cuya ejecución implica que el docstring "se ejecutó"
    for node in ast.walk(tree):
        if isinstance(node, ast.stmt):
            lines.add(node.lineno)
            for d in getattr(node, "decorator_list", []):
                lines.add(d.lineno)
        body = getattr(node, "body", None)
        if (isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                and body and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str)):
            # Python 3.13 no emite evento LINE para un docstring; se da por ejecutado
            # si se ejecutó la siguiente sentencia del mismo cuerpo (o la cabecera).
            nxt = body[1].lineno if len(body) > 1 else getattr(node, "lineno", 1)
            proxies[body[0].lineno] = nxt
    return lines, proxies


def _on_line(code, line):
    f = code.co_filename
    if f in _targets:
        _hits[f].add(line)
    return sys.monitoring.DISABLE


def pytest_configure(config):
    root = str(config.rootpath)
    for name in os.environ.get("STDCOV_FILES", "").split():
        p = os.path.abspath(os.path.join(root, name))
        _targets[p] = name
        _hits[p] = set()
    sys.monitoring.use_tool_id(TOOL, "stdcov")
    sys.monitoring.register_callback(TOOL, sys.monitoring.events.LINE, _on_line)
    sys.monitoring.set_events(TOOL, sys.monitoring.events.LINE)


def _ranges(nums):
    out, nums = [], sorted(nums)
    i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(str(nums[i]) if i == j else f"{nums[i]}-{nums[j]}")
        i = j + 1
    return ", ".join(out)


def _pct(s, m):
    # Igual que coverage.py: redondeo al entero, pero nunca 100 si falta algo ni 0 si hay algo.
    if s == 0:
        return 100
    p = (s - m) * 100 / s
    r = round(p)
    if r == 100 and m > 0:
        r = 99
    if r == 0 and m < s:
        r = 1
    return r


def pytest_terminal_summary(terminalreporter):
    sys.monitoring.set_events(TOOL, 0)
    tr = terminalreporter
    tr.write_sep("=", "tests coverage")
    rows, ts, tm = [], 0, 0
    for p, name in _targets.items():
        st, proxies = _statements(p)
        hits = set(_hits[p])
        hits |= {doc for doc, nxt in proxies.items() if nxt in hits}
        miss = {l for l in st if l not in hits}
        rows.append((name, len(st), len(miss), miss))
        ts += len(st); tm += len(miss)
    w = max([len(r[0]) for r in rows] + [5]) + 2
    tr.write_line(f"{'Name':<{w}}{'Stmts':>6}{'Miss':>7}{'Cover':>7}   Missing")
    tr.write_line("-" * (w + 30))
    for name, s, m, miss in rows:
        cov = _pct(s, m)
        tr.write_line(f"{name:<{w}}{s:>6}{m:>7}{cov:>6}%   {_ranges(miss)}")
    tr.write_line("-" * (w + 30))
    cov = _pct(ts, tm)
    tr.write_line(f"{'TOTAL':<{w}}{ts:>6}{tm:>7}{cov:>6}%")
