import asyncio
import time
from typing import Any

import httpx

# ── Judge0 configuration ────────────────────────────────────────────────────
JUDGE0_BASE_URL = "https://ce.judge0.com"
JUDGE0_SUBMIT_URL = f"{JUDGE0_BASE_URL}/submissions?base64_encoded=false&wait=true"

# ── Language mapping (as required) ──────────────────────────────────────────
LANGUAGE_MAP: dict[str, int] = {
    "python": 71,
    "javascript": 63,
    "cpp": 54,
    "java": 62,
}

MAX_CODE_SIZE = 20000  # characters


def _wrap_code(code: str, language: str) -> str:
    lang = language.lower()
    
    if lang == "python":
        # Don't wrap if they seem to have their own driver
        if "sys.stdin" in code or "input(" in code:
            return code
            
        import json
        return code + f"""
# --- DRIVER START ---
if __name__ == "__main__":
    import sys, json, ast
    try:
        __tree = ast.parse({repr(code)})
        __funcs = [__n.name for __n in ast.walk(__tree) if isinstance(__n, ast.FunctionDef) and not __n.name.startswith('_')]
        if __funcs:
            __func = globals().get(__funcs[-1])
            if __func:
                __data = sys.stdin.read().strip()
                __res = __func(__data)
                if __res is not None:
                    if isinstance(__res, (list, dict)): print(json.dumps(__res).replace(' ', ''))
                    elif isinstance(__res, bool): print('true' if __res else 'false')
                    else: print(__res)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
"""
    elif lang == "javascript":
        if "process.stdin" in code:
            return code
            
        import json
        return code + f"""
// --- DRIVER START ---
try {{
    const __pattern = /function\\s+([a-zA-Z0-9_$]+)/g;
    let __match, __lastName;
    while ((__match = __pattern.exec({json.dumps(code)})) !== null) {{
        __lastName = __match[1];
    }}
    if (__lastName && typeof eval(__lastName) === 'function') {{
        const __func = eval(__lastName);
        process.stdin.resume();
        process.stdin.setEncoding('utf8');
        let __input = '';
        process.stdin.on('data', d => __input += d);
        process.stdin.on('end', () => {{
            const data = __input.trim();
            const res = __func(data);
            if (res !== undefined && res !== null) {{
                if (typeof res === 'object') console.log(JSON.stringify(res).replace(/\\s/g, ''));
                else console.log(res);
            }}
        }});
    }}
}} catch (e) {{
    console.error(e);
    process.exit(1);
}}
"""
    return code


def _first_non_empty(*vals: str | None) -> str:
    for v in vals:
        if v is not None and str(v).strip():
            return str(v).strip()
    return ""


async def execute_code(code: str, language: str, stdin: str = "") -> dict:
    """
    Execute code via Judge0.

    Returns:
      {
        stdout, stderr, exit_code, success, execution_time_ms
      }
    """
    language_key = (language or "").lower()
    language_id = LANGUAGE_MAP.get(language_key)
    if not language_id:
        return {
            "stdout": "",
            "stderr": f"Language '{language}' not supported",
            "exit_code": 1,
            "success": False,
            "execution_time_ms": 0,
        }

    if len(code) > MAX_CODE_SIZE:
        return {
            "stdout": "",
            "stderr": f"Code exceeds {MAX_CODE_SIZE} character limit",
            "exit_code": 1,
            "success": False,
            "execution_time_ms": 0,
        }

    final_code = _wrap_code(code, language_key)

    payload = {
        "source_code": final_code,
        "language_id": language_id,
        "stdin": stdin or "",
    }

    start = time.monotonic()
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(20.0)) as client:
            resp = await client.post(JUDGE0_SUBMIT_URL, json=payload)
            resp.raise_for_status()
            data: dict[str, Any] = resp.json()
    except httpx.TimeoutException:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        return {
            "stdout": "",
            "stderr": "Judge0 request timed out",
            "exit_code": 124,
            "success": False,
            "execution_time_ms": elapsed_ms,
        }
    except httpx.HTTPError as e:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        return {
            "stdout": "",
            "stderr": f"Judge0 error: {str(e)}",
            "exit_code": 1,
            "success": False,
            "execution_time_ms": elapsed_ms,
        }
    except Exception as e:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        return {
            "stdout": "",
            "stderr": str(e),
            "exit_code": 1,
            "success": False,
            "execution_time_ms": elapsed_ms,
        }

    elapsed_ms = int((time.monotonic() - start) * 1000)

    status = (data.get("status") or {}) if isinstance(data.get("status"), dict) else {}
    status_id = status.get("id")

    stdout = (data.get("stdout") or "").rstrip()
    stderr = (data.get("stderr") or "").rstrip()
    compile_output = (data.get("compile_output") or "").rstrip()
    message = (data.get("message") or "").rstrip()

    # Judge0 success: status.id == 3 (Accepted)
    is_accepted = status_id == 3

    combined_err = _first_non_empty(compile_output, stderr, message)
    success = bool(is_accepted) and not combined_err

    # Best-effort exit_code mapping.
    exit_code = data.get("exit_code")
    if isinstance(exit_code, int):
        final_exit = exit_code
    else:
        final_exit = 0 if success else 1

    return {
        "stdout": stdout,
        "stderr": combined_err,
        "exit_code": final_exit,
        "success": success,
        "execution_time_ms": elapsed_ms,
    }


def normalize(s: str) -> str:
    return s.strip().lower().replace(" ", "").replace("\n", "")


def check(actual: str, expected: str) -> bool:
    return normalize(actual) == normalize(expected)


async def run_test_cases(code, language, test_cases, is_hidden=False, time_limit=5) -> list:
    results = []
    for i, tc in enumerate(test_cases):
        # Judge0 handles timeout internally; we keep the parameter for API compatibility.
        result = await execute_code(code, language, tc.get("input", ""))
        passed = check(result["stdout"], tc["expected"])
        item = {
            "case_number": i + 1,
            "passed": passed,
            "hidden": is_hidden,
            "execution_time_ms": result.get("execution_time_ms", 0)
        }
        if not is_hidden:
            item.update({
                "description": tc.get("description", f"Test {i + 1}"),
                "input": tc.get("input", ""),
                "expected": tc["expected"],
                "actual": result["stdout"] if result["stdout"] else result["stderr"],
                "error": result["stderr"] if not result["stdout"] and result["stderr"] else None
            })
        results.append(item)
    return results


async def check_executor_health() -> dict:
    """Lightweight Judge0 reachability check."""
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(5.0)) as client:
            r = await client.get(JUDGE0_BASE_URL)
        return {"status": "running" if r.status_code < 500 else "degraded", "base_url": JUDGE0_BASE_URL}
    except Exception as e:
        return {"status": "offline", "base_url": JUDGE0_BASE_URL, "message": str(e)}
