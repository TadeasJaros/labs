#!/usr/bin/env bash
# Encrypt your TUL alias (first.last) with the course public key. Nothing leaves
# your machine - there is no /encrypt endpoint on purpose: a server that
# encrypts your plaintext has already seen it.
#
# Usage:
#   ./tools/encrypt_me.sh first.last
#
# Windows: run this from Git Bash (it ships with openssl).
# No openssl at all? Run it inside the lab container:
#   docker compose run --rm --entrypoint /work/tools/encrypt_me.sh onboarding first.last

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "usage: $0 <tul_alias>      e.g. $0 jan.novak" >&2
    exit 2
fi

# A TUL alias is lowercase ASCII, first.last, no diacritics. Warn rather than
# refuse: the list of real aliases has surprises in it, and a student mid-lab
# must not be blocked by this check. The warning goes to stderr so that
# `encrypt_me.sh me > file` still writes only the ciphertext.
if ! printf '%s' "$1" | grep -qE '^[a-z][a-z0-9]*(\.[a-z][a-z0-9]*)+$'; then
    echo "warning: '$1' does not look like a TUL alias (expected e.g. jan.novak)." >&2
    echo "         Lowercase ASCII, no diacritics, no spaces, first.last." >&2
    echo "         Encrypting it anyway - but check it, only your teacher can decrypt it." >&2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PUBKEY="${SCRIPT_DIR}/../server/public_key.pem"

if [[ ! -f "$PUBKEY" ]]; then
    echo "error: course public key not found at $PUBKEY - ask your teacher" >&2
    exit 1
fi

# RSA-OAEP with SHA-256. OAEP adds random padding, so running this twice gives
# two different outputs that decrypt to the same alias. That is what stops
# anyone from encrypting a guess and comparing it to what you committed.
printf '%s' "$1" \
    | openssl pkeyutl -encrypt -pubin -inkey "$PUBKEY" \
        -pkeyopt rsa_padding_mode:oaep \
        -pkeyopt rsa_oaep_md:sha256 \
        -pkeyopt rsa_mgf1_md:sha256 \
    | openssl base64 -A
echo
