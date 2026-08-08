"""
BLCH9X2 — Blockchain & Financial Engineering
Assignment A2: Block Construction Lab (block.py)

Implementation of the Block class, canonical serialization commitment scheme,
genesis block initialization, chain linking, and tamper-evidence demo.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import time
from typing import Any

# Standard 64-character hex zero string representing the absence of a parent block
GENESIS_PREVIOUS_HASH: str = "0" * 64


def sha256_string(s: str) -> str:
    """Return the SHA-256 hex digest of a UTF-8 encoded string."""
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def canonical_dumps(obj: Any) -> str:
    """
    Canonical JSON serialization:
    - sort_keys=True: Eliminates key-order variance across Python dicts.
    - separators=(',', ':'): Removes whitespace variance.
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


class Block:
    """Represents a single block in a simplified cryptographic ledger."""

    def __init__(
        self,
        index: int,
        timestamp: int,
        transactions: list[dict[str, Any]],
        previous_hash: str,
        nonce: int = 0,
    ) -> None:
        self.index = int(index)
        self.timestamp = int(timestamp)
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = int(nonce)
        self.hash = self.compute_hash()

    def payload_for_hash(self) -> dict[str, Any]:
        """
        Return material fields that enter the hash commitment.
        CRITICAL: Excludes 'self.hash' to prevent circular dependencies.
        """
        return {
            "index": self.index,
            "nonce": self.nonce,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
        }

    def compute_hash(self) -> str:
        """Computes the SHA-256 commitment of the canonical JSON payload."""
        raw_string = canonical_dumps(self.payload_for_hash())
        return sha256_string(raw_string)

    def to_dict(self) -> dict[str, Any]:
        """Return the complete block representation, including the stored hash."""
        data = self.payload_for_hash()
        data["hash"] = self.hash
        return data


def create_genesis_block(timestamp: int | None = None) -> Block:
    """Creates the root Genesis block (index=0) with hardcoded zero parent hash."""
    ts = int(time.time()) if timestamp is None else int(timestamp)
    return Block(
        index=0,
        timestamp=ts,
        transactions=[],
        previous_hash=GENESIS_PREVIOUS_HASH,
        nonce=0,
    )


def create_linked_block(
    previous: Block,
    transactions: list[dict[str, Any]],
    timestamp: int | None = None,
    nonce: int = 0,
) -> Block:
    """Creates a new child block whose previous_hash matches the parent's stored hash."""
    ts = int(time.time()) if timestamp is None else int(timestamp)
    return Block(
        index=previous.index + 1,
        timestamp=ts,
        transactions=transactions,
        previous_hash=previous.hash,
        nonce=nonce,
    )


def is_hash_valid(block: Block) -> bool:
    """Verifies that the stored block hash equals a fresh recomputation."""
    return block.hash == block.compute_hash()


if __name__ == "__main__":
    print("==================================================")
    print("      BLCH9X2 Assignment A2 Verification")
    print("==================================================\n")

    # 1. Create Genesis Block
    genesis = create_genesis_block(timestamp=1_700_000_000)
    print("[1] Genesis Block Created")
    print(f"    Index        : {genesis.index}")
    print(f"    Previous Hash: {genesis.previous_hash[:16]}...")
    print(f"    Hash         : {genesis.hash}\n")

    # 2. Link Block 1
    sample_tx = [{"amount": 50, "recipient": "Bob", "sender": "Alice"}]
    block1 = create_linked_block(
        genesis, sample_tx, timestamp=1_700_000_100, nonce=1234
    )
    print("[2] Linked Block 1 Created")
    print(f"    Index        : {block1.index}")
    print(f"    Previous Hash: {block1.previous_hash}")
    print(f"    Parent Hash  : {genesis.hash}")
    print(f"    Link Valid?  : {block1.previous_hash == genesis.hash}")
    print(f"    Block Hash   : {block1.hash}\n")

    # 3. Tamper Evidence Demonstration
    print("[3] Tamper Evidence Demonstration")
    tampered = deepcopy(block1)
    stored_claim = tampered.hash

    # Silent transaction alteration
    tampered.transactions[0]["amount"] = 5000
    recomputed_hash = tampered.compute_hash()

    print(f"    Stored Hash Claim : {stored_claim}")
    print(f"    Recomputed Hash   : {recomputed_hash}")
    print(f"    Hashes Match?     : {stored_claim == recomputed_hash}")
    print(f"    is_hash_valid()?  : {is_hash_valid(tampered)}")

    assert stored_claim != recomputed_hash
    assert is_hash_valid(tampered) is False
    print("\n[SUCCESS] Tamper evidence verified. Mismatch correctly detected.")