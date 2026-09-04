# phoenix_einstein_bridge.py
# PhoenixEngine :: PhoenixEinsteinBridge

from combined_cycle import CombinedAnalysisCycle
from einstein_operator_index import SYSTEMATICS_REGISTRY
from higgs_susy_pipeline import HiggsSUSYPipeline


class PhoenixEinsteinBridge:
    """
    Bridges PhoenixEngine nominal operators into EinsteinEngine
    systematics-aware pipelines.
    """

    def __init__(self, registry=None):
        self.phoenix_cycle = CombinedAnalysisCycle()
        self.registry = registry or SYSTEMATICS_REGISTRY
        self.einstein_pipeline = HiggsSUSYPipeline(self.registry)

    def run_nominal(self, higgs_arr, susy_arr):
        """Returns nominal Higgs and SUSY event counts from the Phoenix cycle."""
        return self.phoenix_cycle.run(higgs_arr, susy_arr)

    def run_full(self, higgs_arr, susy_arr):
        """Returns nominal counts together with EinsteinEngine systematics."""
        return self.einstein_pipeline.run(higgs_arr, susy_arr)

    # Prior public names, retained as aliases.
    run_phoenix_nominal = run_nominal
    run_einstein_full = run_full
