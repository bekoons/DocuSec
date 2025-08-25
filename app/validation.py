import re

# Patterns that indicate potential prompt/SQL/code injection
_PROHIBITED_PATTERNS = {
    "SQL keywords": r"(?i)\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|REPLACE|TRUNCATE|UNION|EXECUTE|EXEC)\b",
    "SQL comment": r"(--|/\*|\*/)",
    "Script tag": r"(?i)<script.*?>.*?</script>",
    "Executable code": r"(?i)\b(import|exec|eval|subprocess|os\.system|os\.popen)\b",
}

_POLICY_NAME_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


def validate_input(text: str) -> None:
    """Validate text for potentially malicious patterns.

    Raises:
        ValueError: If suspicious content is detected.
    """
    for reason, pattern in _PROHIBITED_PATTERNS.items():
        if re.search(pattern, text):
            raise ValueError(f"Input rejected: {reason} detected.")


def validate_policy_name(name: str) -> None:
    """Ensure policy names contain only allowed characters."""

    if not _POLICY_NAME_PATTERN.match(name):
        raise ValueError(
            "Invalid policy name. Use only letters, numbers, underscores, and hyphens."
        )
