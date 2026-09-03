from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path


SUPPORTED_RUNNERS = ("codex-native", "claude-native", "claude-code")
SUPPORTED_EFFORTS = ("low", "medium", "high", "xhigh", "max")
ASSIGNMENT_FIELDS = ("runner", "model", "effort", "fast")


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class Assignment:
    runner: str
    model: str
    effort: str
    fast: bool


@dataclass(frozen=True)
class ResolvedConfig:
    schema_version: int
    profile: str
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


def parse_assignment(table: dict[str, object], owner: str) -> Assignment:
    unknown = set(table) - set(ASSIGNMENT_FIELDS)
    if unknown:
        raise ConfigError(f"{owner} has unknown fields: {', '.join(sorted(unknown))}")
    runner = require_string(table, "runner", owner)
    model = require_string(table, "model", owner)
    effort = require_string(table, "effort", owner)
    fast = table.get("fast")
    if runner not in SUPPORTED_RUNNERS:
        raise ConfigError(f"{owner}.runner must be one of {', '.join(SUPPORTED_RUNNERS)}")
    if effort not in SUPPORTED_EFFORTS:
        raise ConfigError(f"{owner}.effort must be one of {', '.join(SUPPORTED_EFFORTS)}")
    if not isinstance(fast, bool):
        raise ConfigError(f"{owner}.fast must be a boolean")
    if runner != "codex-native" and fast:
        raise ConfigError(f"{owner}.fast is supported only by codex-native")
    return Assignment(runner=runner, model=model, effort=effort, fast=fast)


def parse_string_list(table: dict[str, object], key: str, owner: str) -> tuple[str, ...]:
    value = table.get(key)
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item for item in value):
        raise ConfigError(f"{owner}.{key} must be a non-empty string array")
    return tuple(value)


def merge_assignment(base: dict[str, object], override: dict[str, object], owner: str) -> Assignment:
    unknown = set(override) - set(ASSIGNMENT_FIELDS)
    if unknown:
        raise ConfigError(f"{owner} has unknown fields: {', '.join(sorted(unknown))}")
    return parse_assignment({**base, **override}, owner)


def resolve_config(
    profile_override: str | None = None,
    config_path: Path | None = None,
    use_user_config: bool = True,
) -> ResolvedConfig:
    root = repository_root()
    defaults_path = root / "config" / "models.defaults.toml"
    defaults = load_toml(defaults_path)
    schema_version = require_integer(defaults, "schema_version", "defaults")
    default_profile = require_string(defaults, "default_profile", "defaults")
    profiles = parse_string_list(defaults, "profiles", "defaults")
    role_names = parse_string_list(defaults, "roles", "defaults")
    resolved_user_path = config_path or default_user_config_path()
    user: dict[str, object] = {}
    user_loaded = use_user_config and resolved_user_path.exists()
    if user_loaded:
        user = load_toml(resolved_user_path)
        user_schema = user.get("schema_version", schema_version)
        if user_schema != schema_version:
            raise ConfigError(f"user schema_version must be {schema_version}")
    selected_profile = profile_override or user.get("profile") or default_profile
    if not isinstance(selected_profile, str) or selected_profile not in profiles:
        raise ConfigError(f"profile must be one of {', '.join(profiles)}")
    profile_path = root / "config" / "profiles" / f"{selected_profile}.toml"
    profile = load_toml(profile_path)
    if require_integer(profile, "schema_version", f"profile {selected_profile}") != schema_version:
        raise ConfigError(f"profile {selected_profile} has an incompatible schema_version")
    if require_string(profile, "name", f"profile {selected_profile}") != selected_profile:
        raise ConfigError(f"profile file name and declared name differ: {selected_profile}")
    description = require_string(profile, "description", f"profile {selected_profile}")
    profile_roles = require_table(profile, "roles", f"profile {selected_profile}")
    missing = set(role_names) - set(profile_roles)
    extra = set(profile_roles) - set(role_names)
    if missing or extra:
        details = []
        if missing:
            details.append(f"missing {', '.join(sorted(missing))}")
        if extra:
            details.append(f"unknown {', '.join(sorted(extra))}")
        raise ConfigError(f"profile {selected_profile} roles differ from the registry: {'; '.join(details)}")
    user_roles_value = user.get("roles", {})
    if not isinstance(user_roles_value, dict):
        raise ConfigError("user roles must be a table")
    unknown_user_roles = set(user_roles_value) - set(role_names)
    if unknown_user_roles:
        raise ConfigError(f"user configuration has unknown roles: {', '.join(sorted(unknown_user_roles))}")
    resolved: dict[str, Assignment] = {}
    for role_name in role_names:
        base = profile_roles[role_name]
        override = user_roles_value.get(role_name, {})
        if not isinstance(base, dict):
            raise ConfigError(f"profile role {role_name} must be a table")
        if not isinstance(override, dict):
            raise ConfigError(f"user role {role_name} must be a table")
        resolved[role_name] = merge_assignment(base, override, f"roles.{role_name}")
    return ResolvedConfig(
        schema_version=schema_version,
        profile=selected_profile,
        description=description,
        user_config=str(resolved_user_path) if user_loaded else None,
        roles=resolved,
    )


def resolved_payload(config: ResolvedConfig, role: str | None) -> dict[str, object]:
    if role is not None:
        assignment = config.roles.get(role)
        if assignment is None:
            raise ConfigError(f"unknown role: {role}")
        return {
            "schema_version": config.schema_version,
            "profile": config.profile,
            "user_config": config.user_config,
            "role": role,
            "assignment": asdict(assignment),
        }
    return {
        "schema_version": config.schema_version,
        "profile": config.profile,
        "description": config.description,
        "user_config": config.user_config,
        "roles": {name: asdict(value) for name, value in config.roles.items()},
    }


def parse_override(value: str) -> tuple[str, str, object]:
    key, separator, raw = value.partition("=")
    if not separator or "." not in key:
        raise ConfigError("overrides use ROLE.FIELD=VALUE")
    role, field = key.rsplit(".", 1)
    if field not in ASSIGNMENT_FIELDS:
        raise ConfigError(f"unknown assignment field: {field}")
    if field == "fast":
        if raw not in ("true", "false"):
            raise ConfigError("fast override must be true or false")
        parsed: object = raw == "true"
    else:
        if not raw:
            raise ConfigError(f"{role}.{field} cannot be empty")
        parsed = raw
    return role, field, parsed


def toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_user_config(profile: str, override_values: list[str]) -> str:
    registry = resolve_config(profile_override=profile, use_user_config=False)
    overrides: dict[str, dict[str, object]] = {}
    for value in override_values:
        role, field, parsed = parse_override(value)
        if role not in registry.roles:
            raise ConfigError(f"unknown role: {role}")
        overrides.setdefault(role, {})[field] = parsed
    for role, values in overrides.items():
        merge_assignment(asdict(registry.roles[role]), values, f"roles.{role}")
    lines = [f"schema_version = {registry.schema_version}", f"profile = {toml_string(profile)}"]
    for role in registry.roles:
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
    resolve.add_argument("--profile")
    resolve.add_argument("--config", type=Path)
    resolve.add_argument("--no-user-config", action="store_true")
    configure = commands.add_parser("configure")
    configure.add_argument("--profile", required=True)
    configure.add_argument("--set", action="append", default=[])
    configure.add_argument("--output", type=Path)
    configure.add_argument("--dry-run", action="store_true")
    commands.add_parser("profiles")
    return parser


def main(arguments: list[str] | None = None) -> int:
    parser = build_parser()
    options = parser.parse_args(arguments)
    try:
        if options.command == "resolve":
            config = resolve_config(
                profile_override=options.profile,
                config_path=options.config,
                use_user_config=not options.no_user_config,
            )
            print(json.dumps(resolved_payload(config, options.role), indent=2))
            return 0
        if options.command == "profiles":
            defaults = load_toml(repository_root() / "config" / "models.defaults.toml")
            for profile in parse_string_list(defaults, "profiles", "defaults"):
                resolved = resolve_config(profile_override=profile, use_user_config=False)
                print(f"{resolved.profile}\t{resolved.description}")
            return 0
        content = render_user_config(options.profile, options.set)
        if options.dry_run:
            print(content, end="")
            return 0
        output = options.output or default_user_config_path()
        write_user_config(output, content)
        print(json.dumps({"written": str(output), "profile": options.profile, "overrides": len(options.set)}))
        return 0
    except ConfigError as error:
        print(f"mstack-models: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
