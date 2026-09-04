# einstein_master_config.py
# EinsteinEngine :: MasterConfig
# Carolina-Blue Plate — James Paul Stanley Jr.

from einstein_operator_index import OPERATOR_INDEX, SYSTEMATICS_REGISTRY
from einstein_runner import EinsteinRunner
from phoenix_einstein_bridge import PhoenixEinsteinBridge
from cleaner_op import CleanerOp
from browser_cycle import BrowserCycle
from tab_domain_classifier_op import TabDomainClassifierOp
from systematics_plate import SystematicsPlate
from operator_registry import build_default_registry


class EinsteinMasterConfig:
    """
    Central configuration and orchestration for EinsteinEngine.
    Provides:
        - Operator registry
        - Systematics registry
        - Phoenix→Einstein bridge
        - Browser-aware context ops
        - Unified runner
    """

    def __init__(self):
        # Core registries
        self.operator_index = OPERATOR_INDEX
        self.systematics_registry = SYSTEMATICS_REGISTRY
        self.registry = build_default_registry()

        # Core operators
        self.cleaner = CleanerOp()
        self.browser_cycle = BrowserCycle()
        self.domain_classifier = TabDomainClassifierOp()

        # Engine runners (registry-wired)
        self.runner = EinsteinRunner(
            self.registry,
            self.systematics_registry
        )

        # Bridge between PhoenixEngine and EinsteinEngine
        self.bridge = PhoenixEinsteinBridge(
            registry=self.systematics_registry
        )

        # Flattened Codex-contract plate builder
        self.plate_builder = SystematicsPlate(self.systematics_registry)

    # -----------------------------------------------------
    # Browser context integration
    # -----------------------------------------------------
    def load_browser_context(self, raw_tabs):
        """
        raw_tabs: raw string or list from edge_all_open_tabs
        Returns:
            - active tab
            - classified domain
        """
        tabs = self.browser_cycle.run(raw_tabs)
        active = tabs["active_tab"]
        if active is None:
            return {"active_tab": None, "domain": None}
        classified = self.domain_classifier.classify(active)
        return {
            "active_tab": active,
            "domain": classified["category"]
        }

    # -----------------------------------------------------
    # Full Higgs/SUSY pipeline (nominal + systematics)
    # -----------------------------------------------------
    def run_higgs_susy(self, higgs_arr, susy_arr):
        return self.runner.run_higgs_susy(higgs_arr, susy_arr)

    # -----------------------------------------------------
    # Flattened Codex-contract plate
    # -----------------------------------------------------
    def build_plate(self, nominal, higgs_weights=None, susy_weights=None):
        """
        nominal: {"Combined": {"N_Higgs": ..., "N_SUSY": ...}}
        Returns the flattened plate: plate["systematics"][name]["up"|"down"]
        """
        return self.plate_builder.build_from_nominal(
            nominal, higgs_weights, susy_weights
        )

    # -----------------------------------------------------
    # Phoenix nominal + Einstein full systematics
    # -----------------------------------------------------
    def run_bridge(self, higgs_arr, susy_arr):
        return {
            "phoenix_nominal": self.bridge.run_nominal(higgs_arr, susy_arr),
            "einstein_full": self.bridge.run_full(higgs_arr, susy_arr)
        }
