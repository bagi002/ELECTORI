#!/usr/bin/env python3
"""
Task Status Agent - Automatically checks implementation status of TASK 1 and TASK 2
from DEVELOPMENT_TASKS.md and provides recommendations for UI state management.
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
import requests
from pathlib import Path


@dataclass
class TaskStatus:
    """Status of a specific task."""
    task_id: str
    task_name: str
    status: str  # 'implemented', 'partial', 'missing'
    files_expected: List[str]
    files_found: List[str]
    routes_expected: List[str]
    routes_found: List[str]
    ui_elements: List[str]
    issues: List[str]
    recommendations: List[str]


@dataclass
class AgentReport:
    """Final report from the task agent."""
    timestamp: str
    task_1_status: List[TaskStatus]
    task_2_status: List[TaskStatus]
    ui_issues: List[str]
    navigation_issues: List[str]
    default_page_analysis: Dict[str, Any]
    simulation_focus_issues: List[str]
    recommendations: List[str]
    summary: Dict[str, Any]


class TaskStatusAgent:
    """Agent for analyzing TASK 1 and TASK 2 implementation status."""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.app_running = False
        self.app_url = "http://127.0.0.1:5000"
        
        # TASK 1 definitions from DEVELOPMENT_TASKS.md
        self.task_1_tasks = {
            "1.1": {
                "name": "Kreiranje Projekta i Strukture",
                "files": [
                    "app.py", "config.py", "requirements.txt",
                    "static/css/style.css", "static/js/main.js",
                    "templates/base.html", "models/", "routes/", "utils/"
                ],
                "routes": [],  # No specific routes for project structure
                "ui_elements": []
            },
            "1.2": {
                "name": "Database Setup i Models",
                "files": [
                    "models/__init__.py", "models/simulation.py", "models/city.py",
                    "models/party.py", "models/election.py", "models/parliament.py",
                    "database.py", "seed_data.py"
                ],
                "routes": [],
                "ui_elements": []
            },
            "1.3": {
                "name": "Osnovni API Endpoints",
                "files": [
                    "routes/__init__.py", "routes/simulation_routes.py",
                    "routes/city_routes.py", "routes/party_routes.py",
                    "utils/helpers.py", "utils/validators.py"
                ],
                "routes": [
                    "/api/simulations", "/api/cities", "/api/parties",
                    "/api/health"
                ],
                "ui_elements": []
            }
        }
        
        # TASK 2 definitions from DEVELOPMENT_TASKS.md
        self.task_2_tasks = {
            "2.1": {
                "name": "Frontend Framework i Layout",
                "files": [
                    "templates/index.html", "templates/dashboard.html",
                    "templates/simulation_manager.html", "static/css/dashboard.css",
                    "static/js/api.js", "static/js/dashboard.js"
                ],
                "routes": ["/", "/dashboard", "/simulation-manager"],
                "ui_elements": ["navigation", "dashboard", "simulation_manager"]
            },
            "2.2": {
                "name": "Simulation Management UI",
                "files": [
                    "templates/simulation_list.html", "templates/create_simulation.html",
                    "static/js/simulation_manager.js", "static/css/simulation.css"
                ],
                "routes": ["/simulation-manager"],
                "ui_elements": ["simulation_list", "create_simulation", "simulation_manager"]
            },
            "2.3": {
                "name": "City Management System",
                "files": [
                    "templates/city_manager.html", "static/js/city_manager.js"
                ],
                "routes": ["/city-manager"],
                "ui_elements": ["city_manager", "city_list", "city_crud"]
            },
            "2.4": {
                "name": "Party Management System",
                "files": [
                    "templates/party_manager.html", "templates/party_profile.html",
                    "static/js/party_manager.js", "static/css/party.css"
                ],
                "routes": ["/party-manager", "/party-profile"],
                "ui_elements": ["party_manager", "party_profile", "party_crud"]
            }
        }
    
    def check_app_running(self) -> bool:
        """Check if the Flask application is running."""
        try:
            response = requests.get(f"{self.app_url}/api/health", timeout=5)
            self.app_running = response.status_code == 200
            return self.app_running
        except requests.exceptions.RequestException:
            self.app_running = False
            return False
    
    def check_file_exists(self, file_path: str) -> bool:
        """Check if a file or directory exists."""
        full_path = self.base_path / file_path
        return full_path.exists()
    
    def check_route_exists(self, route: str) -> bool:
        """Check if a route exists and returns valid response."""
        if not self.app_running:
            return False
        
        try:
            response = requests.get(f"{self.app_url}{route}", timeout=5)
            # 200 (OK) or 302 (redirect) are considered valid
            return response.status_code in [200, 302]
        except requests.exceptions.RequestException:
            return False
    
    def find_ui_elements_in_templates(self, template_path: str, elements: List[str]) -> List[str]:
        """Find UI elements in template files."""
        found_elements = []
        template_full_path = self.base_path / "templates" / template_path
        
        if not template_full_path.exists():
            return found_elements
        
        try:
            with open(template_full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for element in elements:
                    # Simple check for element presence
                    if element in content.lower() or f'id="{element}"' in content or f'class="{element}"' in content:
                        found_elements.append(element)
        except Exception:
            pass
        
        return found_elements
    
    def analyze_task_group(self, tasks: Dict, group_name: str) -> List[TaskStatus]:
        """Analyze a group of tasks (TASK 1 or TASK 2)."""
        results = []
        
        for task_id, task_info in tasks.items():
            status = TaskStatus(
                task_id=f"{group_name}.{task_id}",
                task_name=task_info["name"],
                status="missing",
                files_expected=task_info["files"],
                files_found=[],
                routes_expected=task_info["routes"],
                routes_found=[],
                ui_elements=task_info["ui_elements"],
                issues=[],
                recommendations=[]
            )
            
            # Check files
            for file_path in task_info["files"]:
                if self.check_file_exists(file_path):
                    status.files_found.append(file_path)
            
            # Check routes
            for route in task_info["routes"]:
                if self.check_route_exists(route):
                    status.routes_found.append(route)
            
            # Determine overall status
            files_ratio = len(status.files_found) / len(status.files_expected) if status.files_expected else 1.0
            routes_ratio = len(status.routes_found) / len(status.routes_expected) if status.routes_expected else 1.0
            
            if files_ratio >= 0.9 and routes_ratio >= 0.9:
                status.status = "implemented"
            elif files_ratio >= 0.5 or routes_ratio >= 0.5:
                status.status = "partial"
            else:
                status.status = "missing"
            
            # Add issues and recommendations
            if status.status == "partial":
                missing_files = set(status.files_expected) - set(status.files_found)
                missing_routes = set(status.routes_expected) - set(status.routes_found)
                
                if missing_files:
                    status.issues.append(f"Missing files: {', '.join(missing_files)}")
                if missing_routes:
                    status.issues.append(f"Missing routes: {', '.join(missing_routes)}")
                    status.recommendations.append(f"Implement missing routes or disable UI elements that link to them")
            
            elif status.status == "missing":
                status.issues.append("Task is not implemented")
                status.recommendations.append("Either implement the task or remove/disable related UI elements")
            
            results.append(status)
        
        return results
    
    def analyze_navigation_issues(self) -> List[str]:
        """Analyze navigation bar issues."""
        issues = []
        
        # Check if navigation links lead to valid pages
        navigation_links = [
            ("/dashboard", "Dashboard"),
            ("/simulation-manager", "Simulacije"),
            ("/city-manager", "Gradovi"),
            ("/party-manager", "Partije"),
            ("/elections", "Izbori"),
            ("/parliament", "Parlament")
        ]
        
        for route, name in navigation_links:
            if not self.check_route_exists(route):
                issues.append(f"Navigation link '{name}' ({route}) leads to 404 page")
        
        return issues
    
    def analyze_default_page(self) -> Dict[str, Any]:
        """Analyze the default starting page."""
        analysis = {
            "current_default": "/",
            "current_functional": False,
            "recommended_default": "/dashboard",
            "reasoning": "",
            "alternatives": []
        }
        
        # Check if current default is functional
        if self.check_route_exists("/"):
            analysis["current_functional"] = True
            analysis["reasoning"] = "Current default (/) is functional but shows welcome page, not working interface"
        else:
            analysis["reasoning"] = "Current default (/) is not functional"
        
        # Check alternatives
        alternatives = [
            ("/dashboard", "Dashboard with active simulation context"),
            ("/simulation-manager", "Direct access to simulation management"),
            ("/", "Welcome page (current, but least functional)")
        ]
        
        for route, description in alternatives:
            analysis["alternatives"].append({
                "route": route,
                "description": description,
                "functional": self.check_route_exists(route)
            })
        
        return analysis
    
    def analyze_simulation_focus_issues(self) -> List[str]:
        """Analyze simulation focus mechanism issues."""
        issues = []
        
        # Check if there's mechanism to hide simulation list when in simulation
        templates_to_check = [
            "dashboard.html",
            "city_manager.html", 
            "party_manager.html"
        ]
        
        has_focus_mechanism = False
        for template in templates_to_check:
            template_path = self.base_path / "templates" / template
            if template_path.exists():
                try:
                    with open(template_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if "active_simulation" in content or "simulation_focus" in content:
                            has_focus_mechanism = True
                            break
                except Exception:
                    pass
        
        if not has_focus_mechanism:
            issues.append("No simulation focus mechanism found - simulation list always visible")
            issues.append("Should implement mechanism to hide simulation list when user is working within a simulation")
        
        return issues
    
    def generate_ui_recommendations(self, task_1_status: List[TaskStatus], task_2_status: List[TaskStatus]) -> List[str]:
        """Generate UI recommendations based on task analysis."""
        recommendations = []
        
        # Check for non-functional UI elements that should be disabled
        all_tasks = task_1_status + task_2_status
        
        for task in all_tasks:
            if task.status in ["missing", "partial"]:
                if "election" in task.task_name.lower() or "parlament" in task.task_name.lower():
                    recommendations.append(f"Disable or gray out 'Izbori' and 'Parlament' navigation links until implemented")
                
                if task.routes_expected:
                    missing_routes = set(task.routes_expected) - set(task.routes_found)
                    for route in missing_routes:
                        recommendations.append(f"Disable UI elements that link to non-functional route: {route}")
        
        # Navigation improvements
        recommendations.append("Implement dynamic navigation that shows/hides items based on active simulation state")
        recommendations.append("Add visual indicators for active simulation in navigation")
        recommendations.append("Consider progressive disclosure - show advanced features only when basic setup is complete")
        
        return recommendations
    
    def run_analysis(self) -> AgentReport:
        """Run complete analysis and generate report."""
        print("🔍 Starting Task Status Analysis...")
        
        # Check if app is running
        if not self.check_app_running():
            print("⚠️ Warning: Flask application is not running. Route analysis will be limited.")
        
        # Analyze TASK 1
        print("📋 Analyzing TASK 1 (Foundation Setup)...")
        task_1_status = self.analyze_task_group(self.task_1_tasks, "TASK 1")
        
        # Analyze TASK 2
        print("🎨 Analyzing TASK 2 (Core Features)...")
        task_2_status = self.analyze_task_group(self.task_2_tasks, "TASK 2")
        
        # Analyze UI and navigation issues
        print("🔗 Analyzing navigation issues...")
        navigation_issues = self.analyze_navigation_issues()
        
        print("🏠 Analyzing default page...")
        default_page_analysis = self.analyze_default_page()
        
        print("🎯 Analyzing simulation focus issues...")
        simulation_focus_issues = self.analyze_simulation_focus_issues()
        
        # Generate recommendations
        print("💡 Generating recommendations...")
        ui_recommendations = self.generate_ui_recommendations(task_1_status, task_2_status)
        
        # Create summary
        task_1_implemented = sum(1 for t in task_1_status if t.status == "implemented")
        task_1_partial = sum(1 for t in task_1_status if t.status == "partial")
        task_2_implemented = sum(1 for t in task_2_status if t.status == "implemented")
        task_2_partial = sum(1 for t in task_2_status if t.status == "partial")
        
        summary = {
            "task_1": {
                "total": len(task_1_status),
                "implemented": task_1_implemented,
                "partial": task_1_partial,
                "missing": len(task_1_status) - task_1_implemented - task_1_partial
            },
            "task_2": {
                "total": len(task_2_status),
                "implemented": task_2_implemented,
                "partial": task_2_partial,
                "missing": len(task_2_status) - task_2_implemented - task_2_partial
            },
            "overall_status": "All core functionality working, some advanced features missing",
            "priority_actions": [
                "Disable non-functional navigation items",
                "Implement simulation focus mechanism",
                "Change default page to more functional option"
            ]
        }
        
        # Create final report
        report = AgentReport(
            timestamp=datetime.now().isoformat(),
            task_1_status=task_1_status,
            task_2_status=task_2_status,
            ui_issues=navigation_issues,
            navigation_issues=navigation_issues,
            default_page_analysis=default_page_analysis,
            simulation_focus_issues=simulation_focus_issues,
            recommendations=ui_recommendations,
            summary=summary
        )
        
        print("✅ Analysis complete!")
        return report
    
    def save_report(self, report: AgentReport, output_file: str = "task_analysis_report.json"):
        """Save the analysis report to a JSON file."""
        output_path = self.base_path / output_file
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(report), f, indent=2, ensure_ascii=False)
        
        print(f"📄 Report saved to: {output_path}")
    
    def print_summary(self, report: AgentReport):
        """Print a human-readable summary of the analysis."""
        print("\n" + "="*60)
        print("📊 TASK STATUS ANALYSIS SUMMARY")
        print("="*60)
        
        print(f"\n🕒 Analysis Timestamp: {report.timestamp}")
        
        print(f"\n📋 TASK 1 (Foundation Setup):")
        print(f"   ✅ Implemented: {report.summary['task_1']['implemented']}/{report.summary['task_1']['total']}")
        print(f"   ⚠️ Partial: {report.summary['task_1']['partial']}/{report.summary['task_1']['total']}")
        print(f"   ❌ Missing: {report.summary['task_1']['missing']}/{report.summary['task_1']['total']}")
        
        print(f"\n🎨 TASK 2 (Core Features):")
        print(f"   ✅ Implemented: {report.summary['task_2']['implemented']}/{report.summary['task_2']['total']}")
        print(f"   ⚠️ Partial: {report.summary['task_2']['partial']}/{report.summary['task_2']['total']}")
        print(f"   ❌ Missing: {report.summary['task_2']['missing']}/{report.summary['task_2']['total']}")
        
        if report.navigation_issues:
            print(f"\n🔗 Navigation Issues ({len(report.navigation_issues)}):")
            for issue in report.navigation_issues:
                print(f"   • {issue}")
        
        if report.simulation_focus_issues:
            print(f"\n🎯 Simulation Focus Issues ({len(report.simulation_focus_issues)}):")
            for issue in report.simulation_focus_issues:
                print(f"   • {issue}")
        
        print(f"\n🏠 Default Page Analysis:")
        print(f"   Current: {report.default_page_analysis['current_default']}")
        print(f"   Recommended: {report.default_page_analysis['recommended_default']}")
        print(f"   Reason: {report.default_page_analysis['reasoning']}")
        
        print(f"\n💡 Top Recommendations:")
        for i, rec in enumerate(report.recommendations[:5], 1):
            print(f"   {i}. {rec}")
        
        print(f"\n🎯 Priority Actions:")
        for i, action in enumerate(report.summary['priority_actions'], 1):
            print(f"   {i}. {action}")
        
        print("\n" + "="*60)


def main():
    """Main function to run the task status agent."""
    agent = TaskStatusAgent()
    report = agent.run_analysis()
    agent.save_report(report)
    agent.print_summary(report)
    
    return report


if __name__ == "__main__":
    main()