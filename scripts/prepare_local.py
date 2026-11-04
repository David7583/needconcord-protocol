"""Create synthetic two-node files with fresh private test credentials; print no secrets."""
import argparse
import json
from pathlib import Path
import secrets

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=ROOT/"runtime/manual")
    parser.add_argument("--port-a", type=int, default=8761)
    parser.add_argument("--port-b", type=int, default=8762)
    args = parser.parse_args()
    if args.port_a == args.port_b or not all(1 <= p <= 65535 for p in (args.port_a, args.port_b)):
        parser.error("two distinct valid ports required")
    folder = args.directory.resolve()
    if not folder.is_relative_to(ROOT/"runtime"):
        parser.error("directory must be inside this project's ignored runtime directory")
    if folder.exists() and any(folder.iterdir()):
        parser.error("use a new empty directory")
    folder.mkdir(parents=True, exist_ok=True)
    token = secrets.token_hex(32)
    for own, peer, peer_port in (("a", "b", args.port_b), ("b", "a", args.port_a)):
        config = {"participant_id": f"test-node-{own}", "peers": {f"test-node-{peer}": {"url": f"http://127.0.0.1:{peer_port}", "token": token}}, "selected_recipients": [f"test-node-{peer}"]}
        (folder/f"{own}.local.json").write_text(json.dumps(config, indent=2)+"\n", encoding="utf-8")
    for name, owner in (("intent.publish.json", "a"), ("proposal.goods.json", "b"), ("proposal.nontransaction.json", "b"), ("outcome.no_purchase.json", "a")):
        packet = json.loads((ROOT/"examples"/name).read_text(encoding="utf-8"))
        packet["sender"] = {"participant_id": f"test-node-{owner}"}
        (folder/name).write_text(json.dumps(packet, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"Created synthetic files in {folder}; credentials remain private. See docs/REFERENCE.md.")

if __name__ == "__main__": main()
