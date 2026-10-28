"""
Validation utilities for patient input features across all disease prediction modules.
"""
from typing import Dict, Any, Tuple, List
from src.utils.constants import HEART_FIELDS, LIVER_FIELDS, KIDNEY_FIELDS, LUNG_FIELDS, BREAST_CANCER_FIELDS

FIELD_SCHEMAS = {
    "heart": HEART_FIELDS,
    "liver": LIVER_FIELDS,
    "kidney": KIDNEY_FIELDS,
    "lung": LUNG_FIELDS,
    "breast_cancer": BREAST_CANCER_FIELDS
}

def validate_input(disease: str, user_input: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validates user input against the schema for a given disease.
    Returns (is_valid, list_of_error_messages).
    """
    if disease not in FIELD_SCHEMAS:
        return False, [f"Unknown disease identifier: '{disease}'"]

    schema = FIELD_SCHEMAS[disease]
    errors = []

    for field_name, rules in schema.items():
        if field_name not in user_input:
            errors.append(f"Missing required parameter: {rules.get('label', field_name)}")
            continue

        val = user_input[field_name]
        field_label = rules.get("label", field_name)

        if val is None or (isinstance(val, str) and str(val).strip() == ""):
            errors.append(f"Field '{field_label}' cannot be empty.")
            continue

        field_type = rules.get("type", "number")

        if field_type in ("number", "float"):
            try:
                num_val = float(val)
                min_val = rules.get("min")
                max_val = rules.get("max")
                if min_val is not None and num_val < min_val:
                    errors.append(f"'{field_label}' ({num_val}) is below the acceptable minimum of {min_val}.")
                if max_val is not None and num_val > max_val:
                    errors.append(f"'{field_label}' ({num_val}) exceeds the acceptable maximum of {max_val}.")
            except (ValueError, TypeError):
                errors.append(f"'{field_label}' must be a valid number.")

        elif field_type == "select":
            options = rules.get("options", [])
            if str(val) not in options:
                errors.append(f"Invalid selection for '{field_label}'. Allowed options: {', '.join(options)}")

    return len(errors) == 0, errors
