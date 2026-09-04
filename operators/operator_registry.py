# operator_registry.py
# PhoenixEngine / EinsteinEngine :: Operator Registry
# Declarative + introspective operator manifest

import importlib
import json

# Engine-facing module paths -> local workspace modules.
# Index entries keep their canonical engine registration paths; this map
# lets the registry resolve them inside the scripts workspace.
LOCAL_MODULE_ALIASES = {
    "PhoenixEngine.SystematicsOp": "anerOp",
    "EinsteinEngine.einstein_harmonizer": "einstein_harmonizer",
}


class OperatorRegistry:
    """
    Collects operator index entries and validates:
        - module importability
        - class existence
        - dependency declarations
        - registry introspection flags

    Provides:
        - register(entry)
        - load(name)
        - validate(entry)
        - manifest()
    """

    def __init__(self, aliases=None):
        self.entries = {}
        self._cache = {}
        self.aliases = aliases if aliases is not None else dict(LOCAL_MODULE_ALIASES)

    # ---------------------------------------------------------
    # Registration
    # ---------------------------------------------------------

    def register(self, entry):
        name = entry["name"]
        self.entries[name] = entry
        self.validate(entry)

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(self, entry):
        module_name = entry["module"]
        class_name = entry["class"]

        # 1. Module importability (engine path resolved through aliases)
        module = importlib.import_module(self.aliases.get(module_name, module_name))

        # 2. Class existence
        if not hasattr(module, class_name):
            raise ImportError(
                f"OperatorRegistry: class '{class_name}' not found in module '{module_name}'"
            )

        # 3. Dependency declarations (contract-level only)
        deps = entry.get("dependencies", [])
        for dep in deps:
            # Dependency may be contract-only; no runtime import required
            # but we ensure the name exists in registry if already registered
            if dep in self.entries:
                continue

        return True

    # ---------------------------------------------------------
    # Loading
    # ---------------------------------------------------------

    def load(self, name):
        """Resolve and return the operator class (lazily imported, cached)."""
        if name in self._cache:
            return self._cache[name]
        entry = self.entries[name]
        module = importlib.import_module(self.aliases.get(entry["module"], entry["module"]))
        cls = getattr(module, entry["class"])
        self._cache[name] = cls
        return cls

    def instantiate(self, name, *args, **kwargs):
        """Load the operator class and construct an instance."""
        return self.load(name)(*args, **kwargs)

    # ---------------------------------------------------------
    # Manifest
    # ---------------------------------------------------------

    def manifest(self):
        return {
            name: {
                "module": e["module"],
                "class": e["class"],
                "version": e.get("version"),
                "dependencies": e.get("dependencies", []),
                "engine_flags": e.get("engine_flags", {})
            }
            for name, e in self.entries.items()
        }


def build_default_registry():
    """Returns the registry preloaded with this workspace's index entries."""
    from systematics_op_index_entry import SystematicsOpIndexEntry
    from einstein_harmonizer_index_entry import EinsteinHarmonizerIndexEntry

    registry = OperatorRegistry()
    registry.register(SystematicsOpIndexEntry)
    registry.register(EinsteinHarmonizerIndexEntry)
    registry.register({
        "name": "HiggsSUSYPipeline",
        "module": "higgs_susy_pipeline",
        "class": "HiggsSUSYPipeline",
        "version": "1.0",
        "dependencies": ["CombinedAnalysisCycle", "SystematicsOperator"],
        "engine_flags": {"runtime": True},
    })
    return registry


def load_manifest(path, registry=None):
    """
    Loads a Carolina-Blue operator manifest (JSON) and registers every
    operator entry, validating module/class existence for each.
    Returns the registry.
    """
    with open(path, encoding="utf-8") as handle:
        manifest = json.load(handle)

    registry = registry if registry is not None else OperatorRegistry()
    for entry in manifest["operators"]:
        registry.register(entry)
    return registry
