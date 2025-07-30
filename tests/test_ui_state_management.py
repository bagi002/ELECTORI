"""
Tests for UI State Management functionality
"""

import pytest
from unittest.mock import patch, MagicMock
from utils.ui_state_manager import UIStateManager, get_ui_context


class TestUIStateManager:
    """Test UI State Manager functionality."""
    
    def test_init_without_report(self):
        """Test initialization without task report."""
        manager = UIStateManager(task_report_path="nonexistent.json")
        assert manager.task_report is None
        
    def test_feature_implementation_status(self):
        """Test feature implementation status detection."""
        manager = UIStateManager()
        
        # Test implemented features
        assert manager._is_feature_implemented("simulation_manager") == True
        assert manager._is_feature_implemented("city_manager") == True
        assert manager._is_feature_implemented("party_manager") == True
        assert manager._is_feature_implemented("dashboard") == True
        
        # Test unimplemented features
        assert manager._is_feature_implemented("elections_nav") == False
        assert manager._is_feature_implemented("parliament_nav") == False
    
    def test_navigation_state(self):
        """Test navigation state generation."""
        manager = UIStateManager()
        nav_state = manager.get_navigation_state()
        
        # Check implemented features are enabled
        assert nav_state["dashboard"] == True
        assert nav_state["simulations"] == True
        assert nav_state["cities"] == True
        assert nav_state["parties"] == True
        
        # Check unimplemented features are disabled
        assert nav_state["elections"] == False
        assert nav_state["parliament"] == False
    
    @patch('utils.ui_state_manager.session')
    def test_simulation_list_visibility_no_active_simulation(self, mock_session):
        """Test simulation list visibility when no active simulation."""
        mock_session.get.return_value = None
        
        manager = UIStateManager()
        assert manager.should_show_simulation_list() == True
    
    @patch('utils.ui_state_manager.session')
    @patch('utils.ui_state_manager.request')
    def test_simulation_list_visibility_with_active_simulation(self, mock_request, mock_session):
        """Test simulation list visibility with active simulation."""
        mock_session.get.return_value = 1
        mock_request.endpoint = 'dashboard'
        
        manager = UIStateManager()
        # Should hide simulation list when working in other parts of the app
        assert manager.should_show_simulation_list() == False
        
        # Should show simulation list when on simulation manager page
        mock_request.endpoint = 'simulation_manager'
        assert manager.should_show_simulation_list() == True
    
    @patch('utils.ui_state_manager.session')
    def test_template_context(self, mock_session):
        """Test template context generation."""
        mock_session.get.return_value = 1
        
        manager = UIStateManager()
        context = manager.get_context_for_template()
        
        assert "ui_state" in context
        assert "navigation" in context["ui_state"]
        assert "active_simulation_id" in context["ui_state"]
        assert "show_simulation_list" in context["ui_state"]
        assert "has_active_simulation" in context["ui_state"]
        
        assert context["ui_state"]["has_active_simulation"] == True
        assert context["ui_state"]["active_simulation_id"] == 1
    
    def test_disabled_features_list(self):
        """Test getting list of disabled features."""
        manager = UIStateManager()
        disabled = manager.get_disabled_features()
        
        assert "elections" in disabled
        assert "parliament" in disabled
        assert "dashboard" not in disabled
        assert "simulations" not in disabled


class TestUIContextIntegration:
    """Test UI context integration with Flask."""
    
    @patch('utils.ui_state_manager.session')
    def test_get_ui_context_function(self, mock_session):
        """Test the get_ui_context helper function."""
        mock_session.get.return_value = None
        
        context = get_ui_context()
        
        assert "ui_state" in context
        assert context["ui_state"]["has_active_simulation"] == False
        assert context["ui_state"]["active_simulation_id"] is None


class TestUIStateManagerWithTaskReport:
    """Test UI State Manager with actual task report."""
    
    def test_with_mock_task_report(self):
        """Test with mocked task report data."""
        mock_report = {
            "task_1_status": [
                {"task_id": "TASK 1.1.1", "status": "implemented"},
                {"task_id": "TASK 1.1.2", "status": "implemented"},
                {"task_id": "TASK 1.1.3", "status": "partial"}
            ],
            "task_2_status": [
                {"task_id": "TASK 2.2.1", "status": "implemented"},
                {"task_id": "TASK 2.2.2", "status": "implemented"},
                {"task_id": "TASK 2.2.3", "status": "implemented"},
                {"task_id": "TASK 2.2.4", "status": "implemented"}
            ]
        }
        
        with patch.object(UIStateManager, '_load_task_report', return_value=mock_report):
            manager = UIStateManager()
            assert manager.task_report is not None
            
            # Navigation state should still work correctly
            nav_state = manager.get_navigation_state()
            assert nav_state["elections"] == False  # Still disabled as it's not implemented
            assert nav_state["parliament"] == False


@pytest.fixture
def app_with_ui_state(app):
    """Fixture that provides app with UI state context processor."""
    @app.context_processor
    def inject_ui_state():
        return get_ui_context()
    
    return app


class TestUIStateIntegrationWithApp:
    """Test UI state integration with Flask app."""
    
    def test_context_processor_injection(self, app_with_ui_state):
        """Test that UI state is properly injected into templates."""
        with app_with_ui_state.test_request_context():
            # This would normally be called during template rendering
            context = get_ui_context()
            
            assert "ui_state" in context
            assert isinstance(context["ui_state"]["navigation"], dict)
    
    def test_template_rendering_with_ui_state(self, app_with_ui_state, client):
        """Test that templates can access UI state."""
        with app_with_ui_state.test_request_context():
            # Simulate template rendering with UI state
            from flask import render_template_string
            
            template = """
            {% if ui_state.navigation.elections %}
                <a href="/elections">Elections</a>
            {% else %}
                <span class="disabled">Elections (Coming Soon)</span>
            {% endif %}
            """
            
            rendered = render_template_string(template)
            assert "Elections (Coming Soon)" in rendered
            assert 'href="/elections"' not in rendered


if __name__ == "__main__":
    pytest.main([__file__])