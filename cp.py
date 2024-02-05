import re

def increment_cluster_alias(cluster_alias):
    pattern = r'(-\d+)?$'
    match = re.search(pattern, cluster_alias)

    if match:
        suffix = match.group(1)
        if suffix is None:
            new_suffix = 1
        else:
            current_suffix = int(suffix[1:])
            new_suffix = (current_suffix + 1) % 100  # Restart from -1 if current suffix is -99

        new_alias = re.sub(pattern, f'-{new_suffix}', cluster_alias)
        return new_alias

# Example usage:
cluster_alias = "a_5ety5g65-5"
new_alias = increment_cluster_alias(cluster_alias)
print(new_alias)
