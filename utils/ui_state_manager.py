"""
UI State Manager - Manages UI element states based on implementation status
"""

from typing import Dict, List, Optional
import json
from pathlib import Path


class UIStateManager:
    """Manages the state of UI elements based on feature implementation status."""
    
    def __init__(self, task_report_path: str = "task_analysis_report.json"):
        self.task_report_path = task_report_path
        self.task_report = self._load_task_report()
        
        # Define which UI elements correspond to which tasks/features
        self.ui_feature_mapping = {
            "elections_nav": {
                "routes": ["/elections"],
                "task_groups": ["TASK 4"],  # Elections are in TASK 4 (not implemented)
                "fallback_status": "disabled"
            },
            "parliament_nav": {
                "routes": ["/parliament"],
                "task_groups": ["TASK 5"],  # Parliament is in TASK 5 (not implemented)
                "fallback_status": "disabled"
            },
            "simulation_manager": {
                "routes": ["/simulation-manager"],
                "task_groups": ["TASK 2.2"],
                "fallback_status": "enabled"
            },
            "city_manager": {
                "routes": ["/city-manager"],
                "task_groups": ["TASK 2.3"],
                "fallback_status": "enabled"
            },
            "party_manager": {
                "routes": ["/party-manager"],
                "task_groups": ["TASK 2.4"],
                "fallback_status": "enabled"
            },
            "dashboard": {
                "routes": ["/dashboard"],
                "task_groups": ["TASK 2.1"],
                "fallback_status": "enabled"
            },
            "support_matrix": {
                "routes": ["/support-matrix"],
                "task_groups": ["TASK 3.1"],  # Support matrix is implemented in TASK 3.1
                "fallback_status": "enabled"
            },
            "support_analytics": {
                "routes": ["/support-analytics"],
                "task_groups": ["TASK 3.2"],  # Support analytics is implemented in TASK 3.2
                "fallback_status": "enabled"
            }
        }
    
    def _load_task_report(self) -> Optional[Dict]:
        """Load the task analysis report."""
        try:
            report_path = Path(self.task_report_path)
            if report_path.exists():
                with open(report_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load task report: {e}")
        return None
    
    def _is_feature_implemented(self, feature_name: str) -> bool:
        """Check if a feature is implemented based on the task report."""
        if not self.task_report:
            # Fallback to conservative approach
            feature_config = self.ui_feature_mapping.get(feature_name, {})
            return feature_config.get("fallback_status") == "enabled"
        
        feature_config = self.ui_feature_mapping.get(feature_name, {})
        
        # Check routes
        if "routes" in feature_config:
            # For now, we'll use a simplified check based on known implementation status
            for route in feature_config["routes"]:
                if route in ["/elections", "/parliament"]:
                    return False  # These are known to be unimplemented
                elif route in ["/dashboard", "/simulation-manager", "/city-manager", "/party-manager", "/support-matrix", "/support-analytics"]:
                    return True  # These are implemented
        
        return feature_config.get("fallback_status") == "enabled"
    
    def get_navigation_state(self) -> Dict[str, bool]:
        """Get the state of navigation elements."""
        return {
            "dashboard": self._is_feature_implemented("dashboard"),
            "simulations": self._is_feature_implemented("simulation_manager"),
            "cities": self._is_feature_implemented("city_manager"),
            "parties": self._is_feature_implemented("party_manager"),
            "support_matrix": self._is_feature_implemented("support_matrix"),
            "support_analytics": self._is_feature_implemented("support_analytics"),
            "elections": self._is_feature_implemented("elections_nav"),
            "parliament": self._is_feature_implemented("parliament_nav")
        }
    
    def should_show_simulation_list(self) -> bool:
        """Determine if simulation list should be shown based on current context."""
        try:
            from flask import session
            active_simulation_id = session.get('active_simulation_id')
        except RuntimeError:
            # Not in request context (e.g., during testing)
            return True
        
        # If no active simulation, always show simulation list
        if not active_simulation_id:
            return True
        
        # If we're on simulation manager page, show list
        try:
            from flask import request
            if request.endpoint in ['simulation_manager', 'index']:
                return True
        except RuntimeError:
            # Not in request context (e.g., during testing)
            pass
        
        # If we're working within a simulation (other pages), hide simulation list
        return False
    
    def get_context_for_template(self) -> Dict:
        """Get context data for templates."""
        try:
            from flask import session
            active_simulation_id = session.get('active_simulation_id')
        except RuntimeError:
            # Not in request context (e.g., during testing)
            active_simulation_id = None
        
        return {
            "ui_state": {
                "navigation": self.get_navigation_state(),
                "active_simulation_id": active_simulation_id,
                "show_simulation_list": self.should_show_simulation_list(),
                "has_active_simulation": bool(active_simulation_id)
            }
        }
    
    def get_disabled_features(self) -> List[str]:
        """Get a list of disabled features."""
        disabled = []
        nav_state = self.get_navigation_state()
        
        for feature, enabled in nav_state.items():
            if not enabled:
                disabled.append(feature)
        
        return disabled


# Global instance
ui_state_manager = UIStateManager()


def get_ui_context():
    """Helper function to get UI context for templates."""
    try:
        return ui_state_manager.get_context_for_template()
    except RuntimeError:
        # Fallback for testing or when not in request context
        return {
            "ui_state": {
                "navigation": {
                    "dashboard": True,
                    "simulations": True,
                    "cities": True,
                    "parties": True,
                    "support_matrix": True,
                    "support_analytics": True,
                    "elections": False,
                    "parliament": False
                },
                "active_simulation_id": None,
                "show_simulation_list": True,
                "has_active_simulation": False
            }
        }