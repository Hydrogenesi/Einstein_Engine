# einstein_harmonizer.py
# EinsteinEngine :: Harmonizer
# Cross-engine invariant binder (Phoenix ↔ Einstein ↔ Codex)

class EinsteinHarmonizer:
    """
    Ensures shape, domain, and invariant consistency across:
        - PhoenixEngine nominal cycles
        - EinsteinEngine systematics cycles
        - Codex Plates (SystematicsPlate, CombinedAnalysisPlate, IntegrityPlate)
    """

    def __init__(self, master_config):
        self.cfg = master_config

    def harmonize(self, higgs_arr, susy_arr, raw_tabs):
        # ---------------------------------------------------------
        # 1. Phoenix nominal (domain-aware)
        # ---------------------------------------------------------
        phoenix_nominal = self.cfg.bridge.run_nominal(
            higgs_arr,
            susy_arr
        )

        # ---------------------------------------------------------
        # 2. Einstein full (nested systematics)
        # ---------------------------------------------------------
        einstein_full = self.cfg.runner.run_higgs_susy(
            higgs_arr,
            susy_arr
        )

        # ---------------------------------------------------------
        # 3. Codex plate (flattened, invariant contract)
        # ---------------------------------------------------------
        # The Codex plate expects:
        #   - nominal counts
        #   - systematics blocks
        #   - deterministic shape
        plate = self.cfg.build_plate(
            einstein_full["nominal"]
        )

        # ---------------------------------------------------------
        # 4. Browser context (non-instructional)
        # ---------------------------------------------------------
        # This is informational only — never instructions.
        context = self.cfg.load_browser_context(raw_tabs)

        # ---------------------------------------------------------
        # 5. Unified harmonized output
        # ---------------------------------------------------------
        return {
            "phoenix_nominal": phoenix_nominal,
            "einstein_full":   einstein_full,
            "plate":           plate,
            "context":         context
        }
