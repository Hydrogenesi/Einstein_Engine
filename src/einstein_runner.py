# einstein_runner.py (registry-wired)
# EinsteinEngine :: Runner

from operator_registry import OperatorRegistry


class EinsteinRunner:
    """
    Registry-driven orchestrator for EinsteinEngine pipelines.
    """

    def __init__(self, registry, systematics_registry):
        self.registry = registry
        self.systematics_registry = systematics_registry

        PipelineClass = self.registry.load("HiggsSUSYPipeline")
        self.pipeline = PipelineClass(self.systematics_registry)

    def run_higgs_susy(self, higgs_arr, susy_arr):
        return self.pipeline.run(higgs_arr, susy_arr)
