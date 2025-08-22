from typing import Dict, List


def map_controls(frameworks: Dict[str, Dict[str, str]], documents: List[str]) -> Dict[str, List[str]]:
    """Naive control mapping by substring matching of control text in documents."""
    mapping: Dict[str, List[str]] = {name: [] for name in frameworks}
    for name, controls in frameworks.items():
        for control_id, control_text in controls.items():
            for doc in documents:
                if control_text.lower() in doc.lower():
                    mapping[name].append(control_id)
                    break
    return mapping

