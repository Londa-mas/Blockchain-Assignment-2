# Blockchain-Assignment-2
## Overview

This repository contains the implementation of a fundamental cryptographic Block data structure for distributed ledgers. The implementation covers:
1. **Material Payload Structuring**: Packaging `index`, `timestamp`, `transactions`, `previous_hash`, and `nonce`.
2. **Canonical JSON Serialization**: Guaranteeing deterministic hash commitments using sorted keys (`sort_keys=True`) and stripped whitespace separators (`separators=(',', ':')`).
3. **Genesis & Linkage Logic**: Building the root block (`index=0`) and cryptographically linking child blocks.
4. **Tamper Evidence Demonstration**: Verification that any post-publication edit to historical payloads invalidates the stored hash claim.

---

## File Structure

* `block.py` — Complete, runnable Python module containing the `Block` class, canonical serialization, genesis constructor, block linking function, and the automated tamper demo.
* `README.md` — Repository documentation and setup instructions.

---

## Canonical Serialization Scheme

To eliminate hashing variance across platforms and execution environments, all payload dictionaries are serialized using:

```python
json.dumps(payload, sort_keys=True, separators=(',', ':'))
```

* **`sort_keys=True`**: Prevents key-insertion order variances across dictionaries.
* **`separators=(',', ':')`**: Strips whitespace padding around structural delimiters.
* **Integer Timestamps**: Timestamps are explicitly cast to integer Unix seconds (`int(time.time())`) to avoid floating-point formatting discrepancies.
* **Hash Exclusion**: The stored `hash` attribute is strictly excluded from `payload_for_hash()` to prevent circular dependencies.

---

## How to Run

### Prerequisites
* Python 3.9+ (uses standard library modules only: `hashlib`, `json`, `time`, `copy`, `typing`).

### Execution Instructions
Run `block.py` directly from your terminal or IDE:

```bash
python block.py
```

