# einstein_harmonizer_index_entry.py
# EinsteinEngine :: OperatorIndexEntry for EinsteinHarmonizer

EinsteinHarmonizerIndexEntry = {
    "name": "EinsteinHarmonizer",
    "module": "EinsteinEngine.einstein_harmonizer",
    "class": "EinsteinHarmonizer",
    "version": "1.0.0",

    "description": (
        "Cross-engine invariant binder ensuring consistency across PhoenixEngine "
        "nominal cycles, EinsteinEngine systematics cycles, and Codex Plates."
    ),

    "dependencies": [
        "PhoenixEinsteinBridge",
        "EinsteinRunner",
        "SystematicsPlate",
        "CombinedAnalysisPlate"
    ],

    "engine_flags": {
        "einstein_runner_ready": True,
        "registry_introspectable": True,
        "cycle_compatible": True
    }
}
