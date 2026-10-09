"""Resolve IBM Quantum API token from Streamlit secrets, env, or local fallback."""
from __future__ import annotations
import os


def get_ibm_token() -> str:
    """Priority: Streamlit secrets → env IBM_QUANTUM_TOKEN / IBM_TOKEN → empty string."""
    try:
        import streamlit as st
        tok = st.secrets.get("IBM_QUANTUM_TOKEN", None) or st.secrets.get("IBM_TOKEN", None)
        if tok:
            return str(tok).strip()
    except Exception:
        pass
    for key in ("IBM_QUANTUM_TOKEN", "IBM_TOKEN", "QISKIT_IBM_TOKEN"):
        val = os.environ.get(key, "").strip()
        if val:
            return val
    return ""


def get_ibm_service():
    """
    Return an authenticated QiskitRuntimeService.
    Tries several channel/instance combinations used by current IBM Quantum accounts.
    """
    from qiskit_ibm_runtime import QiskitRuntimeService

    token = get_ibm_token()
    if not token:
        raise RuntimeError(
            "IBM Quantum API token not found.\n\n"
            "On Streamlit Cloud: App settings → Secrets, add:\n"
            '  IBM_QUANTUM_TOKEN = "your-token"\n\n'
            "Locally: create .streamlit/secrets.toml with the same line,\n"
            "or set environment variable IBM_QUANTUM_TOKEN."
        )

    # (channel, instance) pairs — try until one works
    attempts = [
        ("ibm_quantum_platform", None),           # newest default (no instance)
        ("ibm_quantum_platform", "open-instance"),
        ("ibm_quantum", None),
        ("ibm_quantum", "ibm-q/open/main"),
    ]

    last_err = None
    for channel, instance in attempts:
        try:
            kwargs = {"channel": channel, "token": token}
            if instance:
                kwargs["instance"] = instance
            svc = QiskitRuntimeService(**kwargs)
            # Light touch to verify the session is usable
            _ = svc.backends()
            return svc
        except Exception as e:
            last_err = e
            continue

    raise RuntimeError(
        "Could not connect to IBM Quantum with the provided token.\n"
        f"Last error: {last_err}\n\n"
        "Checks:\n"
        "1. Token is valid at https://quantum.cloud.ibm.com/  (Account → API token)\n"
        "2. Streamlit Secrets key is exactly IBM_QUANTUM_TOKEN\n"
        "3. Account has access to an open plan / instance"
    )


def env_with_ibm_token(base_env: dict | None = None) -> dict:
    """Copy env and inject IBM token so subprocesses (ibm_run.py) can authenticate."""
    env = dict(base_env or os.environ)
    tok = get_ibm_token()
    if tok:
        env["IBM_QUANTUM_TOKEN"] = tok
        env["IBM_TOKEN"] = tok
        env["QISKIT_IBM_TOKEN"] = tok
    return env
