import os
import random
import pandas as pd
import sys

shard_idx = int(os.environ.get("JOB_COMPLETION_INDEX", "0"))
node_name = os.environ.get("NODE_NAME", "unknown-node")
pod_name = os.environ.get("POD_NAME", "unknown-pod")

random.seed(42 + shard_idx)
rows = []
for i in range(100):
    email = f"user{i}@example.com"
    # Introduce deliberate errors
    if random.random() < 0.15:
        email = "malformed-no-at-sign"
    elif random.random() < 0.05:
        email = None
    rows.append((email, "active"))

df = pd.DataFrame(rows, columns=["email", "status"])
file_path = f"shard_{shard_idx}.csv"
df.to_csv(file_path, index=False)

try:
    invalid_count = df['email'].apply(lambda x: pd.isna(x) or '@' not in str(x)).sum()
    print(f"[Node: {node_name} | Pod: {pod_name}] Shard {shard_idx} validation complete. Found {invalid_count} invalid rows.")
except Exception as e:
    print(f"Error validating {file_path}: {e}")
    sys.exit(1)
