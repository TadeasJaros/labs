"""WEA 2026 - Lab 01 onboarding helper.

Two endpoints. Run it, open http://localhost:8000/docs, and use curl.
"""

import hashlib
from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, Response

from status_codes import CLAIMABLE_CODES

app = FastAPI(
    title="WEA 2026 - Lab 01",
    description="Find out which HTTP status code is yours, then find out what it means.",
    version="1.0.0",
)


def code_for(github_handle: str) -> int:
    """Deterministically map a GitHub handle to one of the claimable codes.

    Two students can end up with the same code. That is fine - the code is
    yours to learn, not a seat to reserve.
    """
    digest = hashlib.sha256(github_handle.strip().lower().encode()).hexdigest()
    return CLAIMABLE_CODES[int(digest, 16) % len(CLAIMABLE_CODES)]


@app.get("/slot", summary="Which status code is mine?")
def get_slot(github_handle: str = Query(..., description="Your GitHub username")):
    handle = github_handle.strip().lower()
    if not handle:
        raise HTTPException(status_code=400, detail="github_handle must not be empty")
    code = code_for(handle)
    return {"github_handle": handle, "http_code": code}


@app.get("/status", summary="Respond with the given status code")
def get_status(code: int = Query(..., description="An HTTP status code, e.g. 418")):
    """Answer *with* the requested status code, so you can inspect it with `curl -i`.

    The JSON body carries the official name and a one-line description.
    """
    try:
        status = HTTPStatus(code)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"{code} is not a known HTTP status code")

    if status.value < 200:
        # 1xx are interim responses. h11 refuses to put one on the wire with a
        # body, so answer 400 with an explanation instead of crashing.
        raise HTTPException(
            status_code=400,
            detail=f"{status.value} {status.phrase} is an interim response and cannot be a final answer.",
        )

    if status.value in (204, 205):
        # RFC 9110 15.3.5: a 204 response has no content. Whatever body we set
        # here would be dropped before it reaches the wire, so send none. If
        # this is your code and `curl -i` shows headers and then nothing - that
        # is the correct behaviour, not a broken setup.
        return Response(status_code=status.value)

    return JSONResponse(
        status_code=status.value,
        content={"code": status.value, "name": status.phrase, "description": status.description},
    )


@app.get("/healthz", include_in_schema=False)
def healthz():
    return {"ok": True}
