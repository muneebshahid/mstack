from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path


SUPPORTED_EFFORTS = ("low", "medium", "high", "xhigh", "max")
ASSIGNMENT_FIELDS = ("model", "effort", "fast")
DEFAULT_FIELDS = ("schema_version", "presets", "roles")
PRESET_FIELDS = ("schema_version", "name", "description", "roles")
USER_FIELDS = ("schema_version", "preset", "roles")
LEGACY_ROLE = "consultant_default"


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class Assignment:
    model: str
    effort: str
    fast: bool


@dataclass(frozen=True)
class ResolvedConfig:
    schema_version: int
    preset: str
    description: str
    user_config: str | None
    roles: dict[str, Assignment]


def repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def default_user_config_path() -> Path:
    explicit = os.environ.get("MSTACK_CONFIG")
    if explicit:
        return Path(explicit).expanduser()
    config_root = os.environ.get("XDG_CONFIG_HOME")
    if config_root:
        return Path(config_root).expanduser() / "mstack" / "models.toml"
    return Path.home() / ".config" / "mstack" / "models.toml"


def load_toml(path: Path) -> dict[str, object]:
    try:
        with path.open("rb") as handle:
            value = tomllib.load(handle)
    except FileNotFoundError as error:
        raise ConfigError(f"configuration file does not exist: {path}") from error
    except tomllib.TOMLDecodeError as error:
        raise ConfigError(f"invalid TOML in {path}: {error}") from error
    if not isinstance(value, dict):
        raise ConfigError(f"configuration root must be a table: {path}")
    return value


def require_string(table: dict[str, object], key: str, owner: str) -> str:
    value = table.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"{owner}.{key} must be a non-empty string")
    return value


def require_integer(table: dict[str, object], key: str, owner: str) -> int:
    value = table.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ConfigError(f"{owner}.{key} must be an integer")
    return value


def require_table(table: dict[str, object], key: str, owner: str) -> dict[str, object]:
    value = table.get(key)
    if not isinstance(value, dict):
        raise ConfigError(f"{owner}.{key} must be a table")
    return value


def reject_unknown_fields(
    table: dict[str, object], allowed: tuple[str, ...], owner: str
) -> None:
    unknown = set(table) - set(allowed)
    if not unknown:
        return
    if "runner" in unknown:
        raise ConfigError(
            f"{owner}.runner is no longer supported; remove it and run setup-mstack"
        )
    raise ConfigError(f"{owner} has unknown fields: {', '.join(sorted(unknown))}")


def reject_legacy_role(role: str, owner: str) -> None:
    if role == LEGACY_ROLE:
        raise ConfigError(
            f"{owner} is no longer supported; rename {role} to delegate_default and run setup-mstack"
        )


def parse_assignment_fields(table: dict[str, object], owner: str) -> Assignment:
    reject_unknown_fields(table, ASSIGNMENT_FIELDS, owner)
    model = require_string(table, "model", owner)
    effort = require_string(table, "effort", owner)
    fast = table.get("fast")
    if effort not in SUPPORTED_EFFORTS:
        raise ConfigError(f"{owner}.effort must be one of {', '.join(SUPPORTED_EFFORTS)}")
    if not isinstance(fast, bool):
        raise ConfigError(f"{owner}.fast must be a boolean")
    return Assignment(model=model, effort=effort, fast=fast)


def parse_string_list(table: dict[str, object], key: str, owner: str) -> tuple[str, ...]:
    value = table.get(key)
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
        raise ConfigError(f"{owner}.{key} must be a non-empty string array")
    return tuple(value)


def merge_assignment(base: dict[str, object], override: dict[str, object], owner: str) -> Assignment:
    reject_unknown_fields(override, ASSIGNMENT_FIELDS, owner)
    return parse_assignment_fields({**base, **override}, owner)


def parse_defaults(defaults: dict[str, object]) -> tuple[int, tuple[str, ...], tuple[str, ...]]:
    reject_unknown_fields(defaults, DEFAULT_FIELDS, "defaults")
    schema_version = require_integer(defaults, "schema_version", "defaults")
    presets = parse_string_list(defaults, "presets", "defaults")
    role_names = parse_string_list(defaults, "roles", "defaults")
    return schema_version, presets, role_names


def validate_user_config(
    user: dict[str, object], schema_version: int
) -> dict[str, object]:
    if "profile" in user:
        raise ConfigError(
            "user configuration.profile is no longer supported; replace profile with preset and run setup-mstack"
        )
    reject_unknown_fields(user, USER_FIELDS, "user configuration")
    user_schema = user.get("schema_version", schema_version)
    if user_schema != schema_version:
        raise ConfigError(f"user schema_version must be {schema_version}")
    if "preset" in user:
        require_string(user, "preset", "user configuration")
    user_roles = user.get("roles", {})
    if not isinstance(user_roles, dict):
        raise ConfigError("user roles must be a table")
    for role_name in user_roles:
        reject_legacy_role(role_name, f"roles.{role_name}")
    return user_roles


def complete_user_role(role_name: str, values: dict[str, object]) -> Assignment:
    owner = f"roles.{role_name}"
    missing = [field for field in ASSIGNMENT_FIELDS if field not in values]
    if missing:
        raise ConfigError(
            f"{owner} must define all assignment fields for a new role: {', '.join(missing)}"
        )
    return parse_assignment_fields(values, owner)


def resolve_config(
    preset_override: str | None = None,
    config_path: Path | None = None,
    use_user_config: bool = True,
) -> ResolvedConfig:
    root = repository_root()
    defaults_path = root / "config" / "models.defaults.toml"
    defaults = load_toml(defaults_path)
    schema_version, presets, role_names = parse_defaults(defaults)
    user: dict[str, object] = {}
    user_loaded = False
    if config_path is not None:
        resolved_user_path = config_path
        user = load_toml(resolved_user_path)
        user_loaded = True
    else:
        resolved_user_path = default_user_config_path()
        if use_user_config and resolved_user_path.exists():
            user = load_toml(resolved_user_path)
            user_loaded = True
    user_roles_value = validate_user_config(user, schema_version) if user_loaded else {}
    if preset_override is not None:
        if not preset_override.strip():
            raise ConfigError("explicit preset must be a non-empty string")
        selected_preset = preset_override
    elif user_loaded and "preset" in user:
        selected_preset = require_string(user, "preset", "user configuration")
    else:
        raise ConfigError("No active profile; run setup-mstack")
    if selected_preset not in presets:
        raise ConfigError(f"preset must be one of {', '.join(presets)}")
    preset_path = root / "config" / "presets" / f"{selected_preset}.toml"
    preset = load_toml(preset_path)
    reject_unknown_fields(preset, PRESET_FIELDS, f"preset {selected_preset}")
    if require_integer(preset, "schema_version", f"preset {selected_preset}") != schema_version:
        raise ConfigError(f"preset {selected_preset} has an incompatible schema_version")
    if require_string(preset, "name", f"preset {selected_preset}") != selected_preset:
        raise ConfigError(f"preset file name and declared name differ: {selected_preset}")
    description = require_string(preset, "description", f"preset {selected_preset}")
    preset_roles = require_table(preset, "roles", f"preset {selected_preset}")
    missing = set(role_names) - set(preset_roles)
    extra = set(preset_roles) - set(role_names)
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing {', '.join(sorted(missing))}")
        if extra:
            details.append(f"unknown {', '.join(sorted(extra))}")
        raise ConfigError(f"preset {selected_preset} roles differ from the registry: {'; '.join(details)}")
    resolved: dict[str, Assignment] = {}
    for role_name in role_names:
        base = preset_roles[role_name]
        override = user_roles_value.get(role_name, {})
        if not isinstance(base, dict):
            raise ConfigError(f"preset role {role_name} must be a table")
        if not isinstance(override, dict):
            raise ConfigError(f"user role {role_name} must be a table")
        resolved[role_name] = merge_assignment(base, override, f"roles.{role_name}")
    for role_name, values in user_roles_value.items():
        if role_name in role_names:
            continue
        if not isinstance(values, dict):
            raise ConfigError(f"user role {role_name} must be a table")
        resolved[role_name] = complete_user_role(role_name, values)
    return ResolvedConfig(
        schema_version=schema_version,
        preset=selected_preset,
        description=description,
        user_config=str(resolved_user_path) if user_loaded else None,
        roles=resolved,
    )


def resolved_payload(config: ResolvedConfig, role: str | None) -> dict[str, object]:
    if role is not None:
        assignment = config.roles.get(role)
        if assignment is None:
            reject_legacy_role(role, f"role {role}")
            raise ConfigError(f"unknown role: {role}")
        return {
            "schema_version": config.schema_version,
            "preset": config.preset,
            "user_config": config.user_config,
            "role": role,
            "assignment": asdict(assignment),
        }
    return {
        "schema_version": config.schema_version,
        "preset": config.preset,
        "description": config.description,
        "user_config": config.user_config,
        "roles": {name: asdict(value) for name, value in config.roles.items()},
    }


def parse_override(value: str) -> tuple[str, str, str | bool]:
    key, separator, raw = value.partition("=")
    if not separator or "." not in key:
        raise ConfigError("overrides use ROLE.FIELD=VALUE")
    role, field = key.rsplit(".", 1)
    reject_legacy_role(role, f"role {role}")
    if field not in ASSIGNMENT_FIELDS:
        if field == "runner":
            raise ConfigError(
                "runner overrides are no longer supported; remove runner and run setup-mstack"
            )
        raise ConfigError(f"unknown assignment field: {field}")
    if field == "fast":
        if raw not in ("true", "false"):
            raise ConfigError("fast override must be true or false")
        parsed: str | bool = raw == "true"
    else:
        if not raw:
            raise ConfigError(f"{role}.{field} cannot be empty")
        parsed = raw
    return role, field, parsed


def toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_user_config(preset: str, override_values: list[str]) -> str:
    registry = resolve_config(preset_override=preset, use_user_config=False)
    overrides: dict[str, dict[str, str | bool]] = {}
    for value in override_values:
        role, field, parsed = parse_override(value)
        overrides.setdefault(role, {})[field] = parsed
    for role, values in overrides.items():
        if role in registry.roles:
            merge_assignment(asdict(registry.roles[role]), values, f"roles.{role}")
        else:
            complete_user_role(role, values)
    lines = [f"schema_version = {registry.schema_version}", f"preset = {toml_string(preset)}"]
    for role in (*registry.roles, *[name for name in overrides if name not in registry.roles]):
        values = overrides.get(role)
        if not values:
            continue
        lines.extend(("", f"[roles.{role}]"))
        for field in ASSIGNMENT_FIELDS:
            if field not in values:
                continue
            value = values[field]
            lines.append(f"{field} = {str(value).lower() if isinstance(value, bool) else toml_string(str(value))}")
    return "\n".join(lines) + "\n"


def write_user_config(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(content)
        temporary_path = Path(handle.name)
    try:
        resolve_config(config_path=temporary_path)
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mstack-models")
    commands = parser.add_subparsers(dest="command", required=True)
    resolve = commands.add_parser("resolve")
    resolve.add_argument("--role")
    resolve.add_argument("--preset")
    resolve.add_argument("--config", type=Path)
    resolve.add_argument("--no-user-config", action="store_true")
    configure = commands.add_parser("configure")
    configure.add_argument("--preset", required=True)
    configure.add_argument("--set", action="append", default=[])
    configure.add_argument("--output", type=Path)
    configure.add_argument("--dry-run", action="store_true")
    commands.add_parser("presets")
    return parser


def main(arguments: list[str] | None = None) -> int:
    parser = build_parser()
    options = parser.parse_args(arguments)
    try:
        if options.command == "resolve":
            config = resolve_config(
                preset_override=options.preset,
                config_path=options.config,
                use_user_config=not options.no_user_config,
            )
            print(json.dumps(resolved_payload(config, options.role), indent=2))
            return 0
        if options.command == "presets":
            defaults = load_toml(repository_root() / "config" / "models.defaults.toml")
            _, presets, _ = parse_defaults(defaults)
            for preset in presets:
                resolved = resolve_config(preset_override=preset, use_user_config=False)
                print(f"{resolved.preset}\t{resolved.description}")
            return 0
        content = render_user_config(options.preset, options.set)
        if options.dry_run:
            print(content, end="")
            return 0
        output = options.output or default_user_config_path()
        write_user_config(output, content)
        print(json.dumps({"written": str(output), "preset": options.preset, "overrides": len(options.set)}))
        return 0
    except ConfigError as error:
        print(f"mstack-models: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
