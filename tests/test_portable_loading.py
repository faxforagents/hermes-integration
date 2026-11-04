"""Run unmodified Hermes v0.22.7 source without installing hermes-agent.

Source lives in .coding-agent/hermes-src, fetched from the tagged raw URLs.
Discovery, native parsing, portable parsing, and loader methods are real.
No shim decides manifest.portable or translates MCP configuration.

The fixture documents every substitute for unrelated runtime services.
All shims are scoped to each test through pytest's monkeypatch fixture.
Nothing here launches npx, connects MCP, resolves secrets, or grants approvals.
"""

import contextvars
import importlib
import json
import shutil
import sys
import threading
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".coding-agent" / "hermes-src"


def unexpected(*args, **kwargs):
    raise AssertionError("This runtime service is outside the portable loading proof")


@pytest.fixture
def hermes(monkeypatch, tmp_path):
    """Install import shims and recording sinks, never a portable parser substitute."""

    def shim(name, **attributes):
        module = ModuleType(name)
        module.__dict__.update(attributes)
        monkeypatch.setitem(sys.modules, name, module)
        return module

    # Namespace packages point directly at the fetched, unmodified Python files.
    monkeypatch.syspath_prepend(str(SOURCE))
    shim("hermes_cli", __path__=[str(SOURCE)])
    for name in ("agent", "tools", "hermes_platform"):
        shim(name, __path__=[])
    for name in ("plugins_manifest", "plugins_discovery", "plugins_loader", "agent_plugins"):
        monkeypatch.delitem(sys.modules, f"hermes_cli.{name}", raising=False)

    # Hermes YAML wrappers use PyYAML for these plain mappings and skill frontmatter.
    shim("hermes_yaml", safe_load=yaml.safe_load)
    shim("utils", fast_safe_load=yaml.safe_load)
    shim("agent.skill_utils", yaml_load=yaml.safe_load)

    # These packages declare no capabilities or locales. Fail on unexpected use.
    def empty_capabilities(value, name):
        assert value in (None, [])
        return []

    shim("hermes_cli.plugin_capabilities", VALID_CAPABILITY_IDS=(),
         parse_declared_capabilities=empty_capabilities)
    shim("agent.i18n_layers", is_language_id=unexpected, normalize_language_id=unexpected)

    # Profile home binding is in-memory and all possible data writes stay in tmp_path.
    home = contextvars.ContextVar("test_hermes_home", default=tmp_path / "home")
    shim("hermes_constants", get_hermes_home=home.get,
         set_hermes_home_override=home.set, reset_hermes_home_override=home.reset)

    # Config, legacy Relay, settings, and replacement services are import-only here.
    shim("hermes_cli.config", cfg_get=unexpected)
    shim("hermes_cli.relay_plugin_cutover", LEGACY_RELAY_PLUGIN_KEYS=frozenset(),
         RELAY_PLUGINS_CONFIG_ENV="UNUSED_TEST_RELAY_CONFIG")
    shim("hermes_cli.plugins_state", _plugin_settings_entry=unexpected)
    shim("registration_lifecycle", replacement_coordinator=SimpleNamespace(transaction=unexpected))

    # Trust-only extensions declare no application, liveness, or cost policy.
    # Their parsers must never run. Unregister records real loader cleanup calls.
    unregistered = []
    shim("hermes_platform.declaration", Declaration=object, parse_declaration=unexpected,
         register=unexpected, unregister=unregistered.append)
    shim("tools.mcp_tool_costs", parse_cost_policy=unexpected)

    # LoadedPlugin is a state container. PluginContext records skill registration.
    # Namespacing and real runtime registration are deliberately outside this proof.
    @dataclass
    class LoadedPlugin:
        manifest: object
        enabled: bool = False
        error: str | None = None

    class PluginContext:
        def __init__(self, manifest, manager):
            self.manager = manager

        def register_skill(self, name, skill_md, description, frontmatter):
            self.manager.skills.append((name, skill_md, description, frontmatter))

    shim("hermes_cli.plugins", LoadedPlugin=LoadedPlugin, PluginContext=PluginContext,
         _PLUGINS_DEBUG=False)

    manifest = importlib.import_module("hermes_cli.plugins_manifest")
    discovery = importlib.import_module("hermes_cli.plugins_discovery")
    loader = importlib.import_module("hermes_cli.plugins_loader")
    portable = importlib.import_module("hermes_cli.agent_plugins")

    class Manager(loader.PluginLoaderMixin):
        def __init__(self):
            self.home_path = home.get()
            self._discovery_lock = threading.RLock()
            self._plugins = {}
            self._portable_mcp_servers = {}
            self._portable_mcp_server_plugins = {}
            self.skills = []
            self.registrations = []

        def _track_registration(self, manifest, kind, name, release):
            self.registrations.append((manifest, kind, name, release))

    yield SimpleNamespace(manifest=manifest, discovery=discovery, loader=loader,
                          portable=portable, Manager=Manager, unregistered=unregistered)
    # Imported modules are also removed, so another test cannot inherit shim globals.
    for name in ("plugins_manifest", "plugins_discovery", "plugins_loader", "agent_plugins"):
        sys.modules.pop(f"hermes_cli.{name}", None)


def discover_package(hermes, directory):
    skipped = {p.name for p in directory.parent.iterdir() if p != directory}
    manifests = hermes.discovery.scan_directory(directory.parent, "user", skip_names=skipped)
    assert len(manifests) == 1
    return manifests[0]


def copy_package(tmp_path):
    directory = tmp_path / "plugins" / "faxforagents"
    directory.mkdir(parents=True)
    for name in ("plugin.json", "mcp.json"):
        shutil.copyfile(ROOT / name, directory / name)
    shutil.copytree(ROOT / "skills", directory / "skills")
    return directory


def test_actual_package_discovers_and_loads_portably(hermes):
    assert not (ROOT / "plugin.yaml").exists()
    assert not (ROOT / "plugin.yml").exists()
    assert not (ROOT / "__init__.py").exists()
    manifest = discover_package(hermes, ROOT)
    assert manifest.name == manifest.key == "faxforagents"
    assert manifest.version == "0.1.0"
    assert manifest.path == str(ROOT)
    assert manifest.portable is True
    assert manifest.requires_hermes == ""  # The catalog owns the portable version floor.

    manager = hermes.Manager()
    # Both the path-selection branch and _load_portable_plugin execute unchanged.
    manager._load_plugin(manifest)
    loaded = manager._plugins["faxforagents"]
    assert loaded.enabled is True
    assert loaded.error is None
    assert list(manager._portable_mcp_servers) == ["faxforagents"]
    server = manager._portable_mcp_servers["faxforagents"]
    assert server["command"] == "npx"
    assert server["args"] == ["-y", "faxforagents-mcp@0.4.1"]
    assert server["trust"] == "untrusted"
    assert server["cwd"] == str(ROOT)
    assert server["env"] == {
        "FAXFORAGENTS_API_KEY": "${FAXFORAGENTS_API_KEY}",
        "PLUGIN_ROOT": str(ROOT),
        "PLUGIN_DATA": str(manager.home_path / "plugin-data" / manifest.data_namespace),
    }
    assert manager._portable_mcp_server_plugins == {"faxforagents": "faxforagents"}
    assert len(manager.skills) == 1
    name, skill_md, description, frontmatter = manager.skills[0]
    assert name == "fax-for-agents"
    assert skill_md == ROOT / "skills" / name / "SKILL.md"
    assert description == frontmatter["description"]
    assert [(kind, name) for _, kind, name, _ in manager.registrations] == [
        ("portable_mcp", "faxforagents")
    ]
    manager.registrations[0][3]()
    assert manager._portable_mcp_servers == {}
    assert manager._portable_mcp_server_plugins == {}
    assert hermes.unregistered == ["faxforagents"]


@pytest.mark.parametrize("extra", [{}, {"entrypoint": "plugin.json"}, {"portable": True}])
def test_yaml_precedence_and_unsupported_markers(hermes, tmp_path, extra):
    directory = copy_package(tmp_path)
    data = yaml.safe_load((ROOT / ".coding-agent" / "plugin-before-fix.yaml").read_text())
    data.update(extra)
    (directory / "plugin.yaml").write_text(yaml.safe_dump(data))
    manifest = discover_package(hermes, directory)
    assert manifest.portable is False
    assert manifest.requires_hermes == ">=0.22.7"
    direct = hermes.manifest.parse_manifest_file(directory / "plugin.yaml", directory, "user", "")
    assert direct == manifest
    with pytest.raises(FileNotFoundError, match="No __init__.py"):
        hermes.Manager()._load_directory_module(manifest)


def test_portable_parser_preserves_explicit_secret_placeholder(hermes, tmp_path, monkeypatch):
    # Expansion of arbitrary environment variables belongs to MCP connection setup.
    monkeypatch.setenv("FAXFORAGENTS_API_KEY", "synthetic-test-value")
    monkeypatch.setenv("UNRELATED_TEST_SECRET", "must-not-be-forwarded")
    package = hermes.portable.load_agent_plugin(ROOT, tmp_path / "data")
    assert package.diagnostics == ()
    assert package.server_declarations == {}
    assert package.mcp_servers["faxforagents"]["env"]["FAXFORAGENTS_API_KEY"] == "${FAXFORAGENTS_API_KEY}"
    assert "UNRELATED_TEST_SECRET" not in package.mcp_servers["faxforagents"]["env"]
    assert [skill.name for skill in package.skills] == ["fax-for-agents"]


def test_wrong_mcp_top_level_is_rejected(hermes, tmp_path):
    directory = copy_package(tmp_path)
    path = directory / "mcp.json"
    data = json.loads(path.read_text())
    data["servers"] = data.pop("mcpServers")
    path.write_text(json.dumps(data))
    diagnostics = []
    assert hermes.portable._discover_mcp(directory, tmp_path / "data", diagnostics) == {}
    assert [d.message for d in diagnostics] == ["mcp.json has an invalid top-level shape"]


def test_invalid_trust_disables_plugin(hermes, tmp_path):
    directory = copy_package(tmp_path)
    path = directory / "plugin.json"
    data = json.loads(path.read_text())
    data["extensions"]["com.nousresearch.hermes"]["servers"]["faxforagents"]["trust"] = "invalid"
    path.write_text(json.dumps(data))
    manifest = discover_package(hermes, directory)
    manager = hermes.Manager()
    manager._load_plugin(manifest)
    loaded = manager._plugins["faxforagents"]
    assert loaded.enabled is False
    assert "trust must be 'untrusted' or 'full'" in loaded.error
    assert manager._portable_mcp_servers == {}
    assert manager.skills == []


def test_catalog_retains_portable_compatibility_metadata():
    catalog = yaml.safe_load((ROOT / "catalog/plugin-catalog/faxforagents.yaml").read_text())
    manifest = json.loads((ROOT / "plugin.json").read_text())
    assert catalog["name"] == manifest["name"]
    assert catalog["version"] == manifest["version"]
    assert catalog["requires_hermes"] == ">=0.22.7"
    assert catalog["capabilities"]["requires_env"] == ["FAXFORAGENTS_API_KEY"]
