#!/usr/bin/env python3
"""
Generate a Terraform google_bigquery_dataset resource block from a user-supplied
YAML file, validated against bigquery_dataset_terraform_parameters.json.

Usage:
    python generate_dataset_tf.py \
        --input dataset_input.yaml \
        --schema bigquery_dataset_terraform_parameters.json \
        --output main_generated.tf \
        --resource-name dataset
"""
import argparse
import json
import sys
from collections import OrderedDict

import yaml

# Keys that render as an HCL *attribute* (key = { ... }) rather than a nested
# *block* (key { ... }) -- these are true maps in the provider schema.
MAP_ATTRIBUTE_KEYS = {"labels", "resource_tags", "parameters"}


def load_schema(path):
    with open(path) as f:
        return json.load(f)


def load_user_input(path):
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    # Drop keys the user left blank/null so we don't emit empty fields.
    return {k: v for k, v in data.items() if v is not None and v != ""}


def validate_required(user_input, schema):
    top_level = schema["top_level_arguments"]
    missing = [
        name for name, spec in top_level.items()
        if spec.get("required") and name not in user_input
    ]
    if missing:
        print("Missing required field(s): " + ", ".join(missing), file=sys.stderr)
        sys.exit(1)


def hcl_scalar(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    # Strings: escape quotes/backslashes, keep as an HCL string literal.
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def render_field(key, value, indent):
    pad = "  " * indent

    # Map attribute (labels, resource_tags, external_catalog_dataset_options.parameters)
    if isinstance(value, dict) and key in MAP_ATTRIBUTE_KEYS:
        if not value:
            return ""
        lines = [f"{pad}{key} = {{"]
        for k, v in value.items():
            lines.append(f"{pad}  {k} = {hcl_scalar(v)}")
        lines.append(f"{pad}}}")
        return "\n".join(lines)

    # Nested block, single instance (dict)
    if isinstance(value, dict):
        inner = "\n".join(
            render_field(k, v, indent + 1) for k, v in value.items()
        )
        inner = "\n".join(line for line in inner.splitlines() if line.strip())
        return f"{pad}{key} {{\n{inner}\n{pad}}}"

    # Repeated blocks (e.g. access: [ {...}, {...} ]) vs. plain string list
    if isinstance(value, list):
        if value and isinstance(value[0], dict):
            return "\n".join(render_field(key, item, indent) for item in value)
        items = ", ".join(hcl_scalar(v) for v in value)
        return f"{pad}{key} = [{items}]"

    # Plain scalar attribute
    return f"{pad}{key} = {hcl_scalar(value)}"


def build_resource_block(user_input, schema, resource_name):
    ordered_keys = list(schema["top_level_arguments"].keys())
    # Preserve schema order for known keys, then append anything extra the user added.
    keys_in_order = [k for k in ordered_keys if k in user_input]
    keys_in_order += [k for k in user_input if k not in ordered_keys]

    body_parts = []
    prev_was_block = None
    for key in keys_in_order:
        value = user_input[key]
        is_block = isinstance(value, dict) and key not in MAP_ATTRIBUTE_KEYS
        is_block = is_block or (isinstance(value, list) and value and isinstance(value[0], dict))
        rendered = render_field(key, value, indent=1)
        if not rendered.strip():
            continue
        if body_parts and (is_block or prev_was_block):
            body_parts.append("")  # blank line before/after blocks for readability
        body_parts.append(rendered)
        prev_was_block = is_block

    body = "\n".join(body_parts)
    return f'resource "google_bigquery_dataset" "{resource_name}" {{\n{body}\n}}\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to user YAML input")
    parser.add_argument(
        "--schema",
        default="bigquery_dataset_terraform_parameters.json",
        help="Path to the reference JSON schema",
    )
    parser.add_argument(
        "--output", default="main_generated.tf", help="Path to write the .tf file"
    )
    parser.add_argument(
        "--resource-name", default="dataset", help="Terraform resource local name"
    )
    args = parser.parse_args()

    schema = load_schema(args.schema)
    user_input = load_user_input(args.input)

    validate_required(user_input, schema)

    tf_code = build_resource_block(user_input, schema, args.resource_name)

    with open(args.output, "w") as f:
        f.write(tf_code)

    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
