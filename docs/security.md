# Security

FastAPI validates input shape and size, limits requests by source address, restricts methods/headers via CORS, and supplies no-store, frame-denial, no-sniff and no-referrer headers. The extension has a strict MV3 CSP, no remote code, and communicates through message passing. Password verifiers use PBKDF2-SHA-256 with random salts and 210,000 iterations; plaintext is never saved. PBKDF2 is used because Web Crypto is native to MV3—use a reviewed Argon2 WASM implementation if policy requires Argon2id.
