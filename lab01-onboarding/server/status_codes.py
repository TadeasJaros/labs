"""Status codes a student can be assigned in Lab 01, and the languages they can declare.

1xx codes and 304 are deliberately not here. A 1xx response is an interim
response - a server cannot send one as a final answer with a body, and trying
to crashes the HTTP layer underneath FastAPI. 304 only makes sense as the
answer to a conditional request. 204 IS here, on purpose; see /status in main.py.
"""

CLAIMABLE_CODES: list[int] = [
    # 2xx Success
    200, 201, 202, 203, 204, 205, 206, 207, 208, 226,
    # 3xx Redirection
    300, 301, 302, 303, 307, 308,
    # 4xx Client Error
    400, 401, 402, 403, 404, 405, 406, 407, 408, 409,
    410, 411, 412, 413, 414, 415, 416, 417, 418, 421,
    422, 423, 424, 425, 426, 428, 429, 431, 451,
    # 5xx Server Error
    500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511,
]

PREFERRED_LANGUAGES: list[str] = [
    "csharp", "typescript", "javascript", "python", "java",
    "kotlin", "go", "rust", "ruby", "other",
]
