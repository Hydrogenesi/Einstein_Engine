# EinsteinEngine :: Operator Index

from browser_cycle import BrowserCycle
from cleaner_op import CleanerOp
from combined_cycle import CombinedAnalysisCycle
from systematics_operator import SystematicsOperator
from systematics_registry_entry import SystematicsRegistryEntry
from tab_domain_classifier_op import TabDomainClassifierOp

OPERATOR_INDEX = {
    "CleanerOp": CleanerOp,
    "BrowserCycle": BrowserCycle,
    "TabDomainClassifierOp": TabDomainClassifierOp,
    "CombinedAnalysisCycle": CombinedAnalysisCycle,
    "SystematicsOperator": SystematicsOperator,
}

SYSTEMATICS_REGISTRY = [
    SystematicsRegistryEntry("JES", 0.05, "SUSY").as_dict(),
    SystematicsRegistryEntry("JER", 0.03, "SUSY").as_dict(),
    SystematicsRegistryEntry("PhotonScale", 0.01, "Higgs").as_dict(),
    SystematicsRegistryEntry("PhotonResolution", 0.02, "Higgs").as_dict(),
    SystematicsRegistryEntry("Pileup", 0.05, "weights").as_dict(),
]