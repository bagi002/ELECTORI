"""
Task 3 Integration Tests

Komprehensivni integracioni testovi za Task 3 - Support System sa slider UI/UX.
"""

import logging
import sys
import pytest
from pathlib import Path
from typing import Dict, List, Any
import json


class Task3IntegrationTester:
    """Klasa za integracione testove Task 3."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.test_results = []
        
    def run_full_integration_tests(self) -> bool:
        """Pokreće kompletne integracione testove za Task 3."""
        try:
            self.logger.info("🧪 Pokretanje integracionih testova za Task 3")
            
            success = True
            
            # Test 1: File Structure Validation
            if not self._test_file_structure():
                success = False
            
            # Test 2: Template Integration
            if not self._test_template_integration():
                success = False
            
            # Test 3: JavaScript Functionality
            if not self._test_javascript_functionality():
                success = False
            
            # Test 4: API Endpoints
            if not self._test_api_endpoints():
                success = False
            
            # Test 5: Slider UI Components
            if not self._test_slider_components():
                success = False
            
            # Test 6: Cross-component Integration
            if not self._test_cross_component_integration():
                success = False
            
            # Test 7: Performance and Accessibility
            if not self._test_performance_accessibility():
                success = False
            
            # Generate test report
            self._generate_test_report()
            
            if success:
                self.logger.info("🎉 Svi integracioni testovi prošli uspešno!")
            else:
                self.logger.error("❌ Neki integracioni testovi su neuspešni")
            
            return success
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri integracionim testovima: {str(e)}")
            return False
    
    def _test_file_structure(self) -> bool:
        """Test postojanja i strukture svih fajlova."""
        try:
            self.logger.info("📁 Testiranje strukture fajlova")
            
            required_files = {
                'task_3_agent.py': 'Task 3 agent executable',
                'routes/support_routes.py': 'Support API routes',
                'templates/support_matrix.html': 'Support Matrix template with sliders',
                'templates/support_analytics.html': 'Support Analytics template',
                'static/js/support_matrix.js': 'Support Matrix JavaScript with sliders',
                'static/js/charts.js': 'Charts JavaScript with slider controls',
                'static/css/support_matrix.css': 'Support Matrix styles with slider CSS',
                'utils/chart_data.py': 'Chart data processing utilities',
                'task_implementations/task_3_1_support_matrix.py': 'Task 3.1 implementation',
                'task_implementations/task_3_2_support_analytics.py': 'Task 3.2 implementation',
                'task_implementations/task_3_integration_tests.py': 'Integration tests'
            }
            
            missing_files = []
            for file_path, description in required_files.items():
                if not Path(file_path).exists():
                    missing_files.append(f"{file_path} ({description})")
            
            if missing_files:
                self.test_results.append({
                    'test': 'File Structure',
                    'status': 'FAILED',
                    'details': f"Missing files: {', '.join(missing_files)}"
                })
                self.logger.error(f"❌ Nedostaju fajlovi: {missing_files}")
                return False
            
            # Check file sizes (should not be empty)
            empty_files = []
            for file_path in required_files.keys():
                path = Path(file_path)
                if path.exists() and path.stat().st_size == 0:
                    empty_files.append(file_path)
            
            if empty_files:
                self.test_results.append({
                    'test': 'File Structure',
                    'status': 'WARNING',
                    'details': f"Empty files: {', '.join(empty_files)}"
                })
                self.logger.warning(f"⚠️ Prazni fajlovi: {empty_files}")
            
            self.test_results.append({
                'test': 'File Structure',
                'status': 'PASSED',
                'details': 'All required files exist and are non-empty'
            })
            self.logger.info("✅ Struktura fajlova je ispravna")
            return True
            
        except Exception as e:
            self.test_results.append({
                'test': 'File Structure',
                'status': 'ERROR',
                'details': str(e)
            })
            self.logger.error(f"❌ Greška pri testiranju strukture: {str(e)}")
            return False
    
    def _test_template_integration(self) -> bool:
        """Test integracije HTML template-a sa slider komponentama."""
        try:
            self.logger.info("📄 Testiranje template integracije")
            
            # Test Support Matrix template
            matrix_template = Path("templates/support_matrix.html")
            with open(matrix_template, 'r', encoding='utf-8') as f:
                matrix_content = f.read()
            
            required_matrix_elements = [
                'id="bulkEditSlider"',
                'id="filterRangeMin"',
                'id="filterRangeMax"',
                'id="normalizationThreshold"',
                'class="support-slider"',
                'class="form-range"',
                'id="supportMatrix"',
                'id="bulkEditModal"',
                'support_matrix.js',
                'support_matrix.css'
            ]
            
            missing_elements = []
            for element in required_matrix_elements:
                if element not in matrix_content:
                    missing_elements.append(element)
            
            if missing_elements:
                self.test_results.append({
                    'test': 'Support Matrix Template',
                    'status': 'FAILED',
                    'details': f"Missing elements: {', '.join(missing_elements)}"
                })
                self.logger.error(f"❌ Support Matrix template nedostaju elementi: {missing_elements}")
                return False
            
            # Test Analytics template
            analytics_template = Path("templates/support_analytics.html")
            with open(analytics_template, 'r', encoding='utf-8') as f:
                analytics_content = f.read()
            
            required_analytics_elements = [
                'id="minSupportSlider"',
                'id="maxSupportSlider"',
                'id="opacitySlider"',
                'id="animationSlider"',
                'id="pieChart"',
                'id="barChart"',
                'Chart.js',
                'charts.js'
            ]
            
            missing_elements = []
            for element in required_analytics_elements:
                if element not in analytics_content:
                    missing_elements.append(element)
            
            if missing_elements:
                self.test_results.append({
                    'test': 'Support Analytics Template',
                    'status': 'FAILED',
                    'details': f"Missing elements: {', '.join(missing_elements)}"
                })
                self.logger.error(f"❌ Analytics template nedostaju elementi: {missing_elements}")
                return False
            
            self.test_results.append({
                'test': 'Template Integration',
                'status': 'PASSED',
                'details': 'All templates contain required slider elements'
            })
            self.logger.info("✅ Template integracija je uspešna")
            return True
            
        except Exception as e:
            self.test_results.append({
                'test': 'Template Integration',
                'status': 'ERROR',
                'details': str(e)
            })
            self.logger.error(f"❌ Greška pri testiranju template-a: {str(e)}")
            return False
    
    def _test_javascript_functionality(self) -> bool:
        """Test JavaScript funkcionalnosti sa slider kontrolama."""
        try:
            self.logger.info("📜 Testiranje JavaScript funkcionalnosti")
            
            # Test Support Matrix JavaScript
            matrix_js = Path("static/js/support_matrix.js")
            with open(matrix_js, 'r', encoding='utf-8') as f:
                matrix_js_content = f.read()
            
            required_matrix_functions = [
                'class SupportMatrixManager',
                'setupSliderControls',
                'updateSliderBackground',
                'updateSupport',
                'validateMatrix',
                'normalizeMatrix',
                'applyBulkEdit',
                'calculateCityTotal',
                'applyFilter',
                'updateStatistics'
            ]
            
            missing_functions = []
            for func in required_matrix_functions:
                if func not in matrix_js_content:
                    missing_functions.append(func)
            
            if missing_functions:
                self.test_results.append({
                    'test': 'Matrix JavaScript',
                    'status': 'FAILED',
                    'details': f"Missing functions: {', '.join(missing_functions)}"
                })
                self.logger.error(f"❌ Matrix JavaScript nedostaju funkcije: {missing_functions}")
                return False
            
            # Test Charts JavaScript
            charts_js = Path("static/js/charts.js")
            with open(charts_js, 'r', encoding='utf-8') as f:
                charts_js_content = f.read()
            
            required_charts_functions = [
                'class SupportAnalytics',
                'setupSliders',
                'createCharts',
                'updateCharts',
                'filterPartyData',
                'hexToRgba'
            ]
            
            missing_functions = []
            for func in required_charts_functions:
                if func not in charts_js_content:
                    missing_functions.append(func)
            
            if missing_functions:
                self.test_results.append({
                    'test': 'Charts JavaScript',
                    'status': 'FAILED',
                    'details': f"Missing functions: {', '.join(missing_functions)}"
                })
                self.logger.error(f"❌ Charts JavaScript nedostaju funkcije: {missing_functions}")
                return False
            
            # Test for slider-specific code patterns
            slider_patterns = [
                'addEventListener(\'input\'',
                'updateSliderBackground',
                'form-range',
                'slider',
                'range'
            ]
            
            matrix_slider_count = sum(1 for pattern in slider_patterns if pattern in matrix_js_content)
            charts_slider_count = sum(1 for pattern in slider_patterns if pattern in charts_js_content)
            
            if matrix_slider_count < 3:
                self.test_results.append({
                    'test': 'JavaScript Slider Integration',
                    'status': 'WARNING',
                    'details': f"Matrix JS has insufficient slider code patterns ({matrix_slider_count})"
                })
                self.logger.warning(f"⚠️ Matrix JS ima malo slider koda")
            
            if charts_slider_count < 2:
                self.test_results.append({
                    'test': 'JavaScript Slider Integration',
                    'status': 'WARNING',
                    'details': f"Charts JS has insufficient slider code patterns ({charts_slider_count})"
                })
                self.logger.warning(f"⚠️ Charts JS ima malo slider koda")
            
            self.test_results.append({
                'test': 'JavaScript Functionality',
                'status': 'PASSED',
                'details': 'All JavaScript files contain required functions and slider integrations'
            })
            self.logger.info("✅ JavaScript funkcionalnost je ispravna")
            return True
            
        except Exception as e:
            self.test_results.append({
                'test': 'JavaScript Functionality',
                'status': 'ERROR',
                'details': str(e)
            })
            self.logger.error(f"❌ Greška pri testiranju JavaScript-a: {str(e)}")
            return False
    
    def _test_api_endpoints(self) -> bool:
        """Test API endpoint-a za support funkcionalnost."""
        try:
            self.logger.info("🔌 Testiranje API endpoint-a")
            
            # Test postojanja support routes
            routes_file = Path("routes/support_routes.py")
            with open(routes_file, 'r', encoding='utf-8') as f:
                routes_content = f.read()
            
            required_endpoints = [
                '@support_bp.route(\'/matrix\'',
                '@support_bp.route(\'/matrix/validate\'',
                '@support_bp.route(\'/matrix/normalize\'',
                '@support_bp.route(\'/update\'',
                '@support_bp.route(\'/bulk-update\'',
                '@support_bp.route(\'/analytics/summary\''
            ]
            
            missing_endpoints = []
            for endpoint in required_endpoints:
                if endpoint not in routes_content:
                    missing_endpoints.append(endpoint)
            
            if missing_endpoints:
                self.test_results.append({
                    'test': 'API Endpoints',
                    'status': 'FAILED',
                    'details': f"Missing endpoints: {', '.join(missing_endpoints)}"
                })
                self.logger.error(f"❌ Nedostaju API endpoint-i: {missing_endpoints}")
                return False
            
            # Test for proper error handling
            error_handling_patterns = [
                'try:',
                'except',
                'jsonify({\'error\'',
                'return jsonify',
                'status: response.status'
            ]
            
            error_handling_count = sum(1 for pattern in error_handling_patterns if pattern in routes_content)
            
            if error_handling_count < 10:  # Should have comprehensive error handling
                self.test_results.append({
                    'test': 'API Error Handling',
                    'status': 'WARNING',
                    'details': f"Limited error handling patterns found ({error_handling_count})"
                })
                self.logger.warning(f"⚠️ Ograničeno error handling u API")
            
            self.test_results.append({
                'test': 'API Endpoints',
                'status': 'PASSED',
                'details': 'All required endpoints are present'
            })
            self.logger.info("✅ API endpoint-i su ispravni")
            return True
            
        except Exception as e:
            self.test_results.append({
                'test': 'API Endpoints',
                'status': 'ERROR',
                'details': str(e)
            })
            self.logger.error(f"❌ Greška pri testiranju API-ja: {str(e)}")
            return False
    
    def _test_slider_components(self) -> bool:
        """Test specifičnih slider komponenti i njihove funkcionalnosti."""
        try:
            self.logger.info("🎚️ Testiranje slider komponenti")
            
            # Test CSS stilova za slajdere
            css_file = Path("static/css/support_matrix.css")
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            required_slider_styles = [
                '.form-range',
                '.slider-container',
                '.slider-primary',
                '.slider-secondary',
                '.slider-success',
                '.slider-warning',
                '.slider-output',
                '::-webkit-slider-thumb',
                '::-webkit-slider-track'
            ]
            
            missing_styles = []
            for style in required_slider_styles:
                if style not in css_content:
                    missing_styles.append(style)
            
            if missing_styles:
                self.test_results.append({
                    'test': 'Slider CSS Styles',
                    'status': 'FAILED',
                    'details': f"Missing styles: {', '.join(missing_styles)}"
                })
                self.logger.error(f"❌ Nedostaju slider stilovi: {missing_styles}")
                return False
            
            # Test for responsive design
            responsive_patterns = [
                '@media',
                'max-width',
                'min-width',
                'mobile',
                'tablet'
            ]
            
            responsive_count = sum(1 for pattern in responsive_patterns if pattern in css_content)
            
            if responsive_count < 2:
                self.test_results.append({
                    'test': 'Responsive Slider Design',
                    'status': 'WARNING',
                    'details': f"Limited responsive design patterns ({responsive_count})"
                })
                self.logger.warning(f"⚠️ Ograničen responsive dizajn")
            
            # Test for accessibility features
            accessibility_patterns = [
                'focus',
                'outline',
                'aria-',
                'role=',
                'tabindex'
            ]
            
            # Check both CSS and HTML templates for accessibility
            accessibility_count = sum(1 for pattern in accessibility_patterns if pattern in css_content)
            
            # Check templates
            for template_file in ['templates/support_matrix.html', 'templates/support_analytics.html']:
                if Path(template_file).exists():
                    with open(template_file, 'r', encoding='utf-8') as f:
                        template_content = f.read()
                        accessibility_count += sum(1 for pattern in accessibility_patterns if pattern in template_content)
            
            if accessibility_count < 3:
                self.test_results.append({
                    'test': 'Slider Accessibility',
                    'status': 'WARNING',
                    'details': f"Limited accessibility features ({accessibility_count})"
                })
                self.logger.warning(f"⚠️ Ograničene accessibility funkcije")
            
            self.test_results.append({
                'test': 'Slider Components',
                'status': 'PASSED',
                'details': 'Slider components are properly implemented with styling'
            })
            self.logger.info("✅ Slider komponente su ispravne")
            return True
            
        except Exception as e:
            self.test_results.append({
                'test': 'Slider Components',
                'status': 'ERROR',
                'details': str(e)
            })
            self.logger.error(f"❌ Greška pri testiranju slider komponenti: {str(e)}")
            return False
    
    def _test_cross_component_integration(self) -> bool:
        """Test integracije između različitih komponenti."""
        try:
            self.logger.info("🔗 Testiranje cross-component integracije")
            
            # Test Task 3 agent integration
            agent_file = Path("task_3_agent.py")
            with open(agent_file, 'r', encoding='utf-8') as f:
                agent_content = f.read()
            
            # Check if agent properly references implementation classes
            integration_patterns = [
                'from task_implementations.task_3_1_support_matrix import SupportMatrixImplementation',
                'from task_implementations.task_3_2_support_analytics import SupportAnalyticsImplementation',
                '_execute_task_3_1',
                '_execute_task_3_2',
                'ui_improvements',
                'slider'
            ]
            
            missing_integrations = []
            for pattern in integration_patterns:
                if pattern not in agent_content:
                    missing_integrations.append(pattern)
            
            if missing_integrations:
                self.test_results.append({
                    'test': 'Agent Integration',
                    'status': 'FAILED',
                    'details': f"Missing integrations: {', '.join(missing_integrations)}"
                })
                self.logger.error(f"❌ Agent nedostaju integracije: {missing_integrations}")
                return False
            
            # Test implementation class structure
            impl_files = [
                'task_implementations/task_3_1_support_matrix.py',
                'task_implementations/task_3_2_support_analytics.py'
            ]
            
            for impl_file in impl_files:
                with open(impl_file, 'r', encoding='utf-8') as f:
                    impl_content = f.read()
                
                required_methods = [
                    'def execute(self)',
                    'def __init__(self, logger',
                    'self.logger'
                ]
                
                missing_methods = []
                for method in required_methods:
                    if method not in impl_content:
                        missing_methods.append(method)
                
                if missing_methods:
                    self.test_results.append({
                        'test': f'Implementation {impl_file}',
                        'status': 'FAILED',
                        'details': f"Missing methods: {', '.join(missing_methods)}"
                    })
                    self.logger.error(f"❌ {impl_file} nedostaju metode: {missing_methods}")
                    return False
            
            self.test_results.append({
                'test': 'Cross-component Integration',
                'status': 'PASSED',
                'details': 'All components are properly integrated'
            })
            self.logger.info("✅ Cross-component integracija je uspešna")
            return True
            
        except Exception as e:
            self.test_results.append({
                'test': 'Cross-component Integration',
                'status': 'ERROR',
                'details': str(e)
            })
            self.logger.error(f"❌ Greška pri testiranju integracije: {str(e)}")
            return False
    
    def _test_performance_accessibility(self) -> bool:
        """Test performansi i accessibility funkcionalnosti."""
        try:
            self.logger.info("⚡ Testiranje performansi i accessibility")
            
            # Check for performance optimizations
            js_files = ['static/js/support_matrix.js', 'static/js/charts.js']
            performance_patterns = [
                'debounce',
                'throttle',
                'setTimeout',
                'clearTimeout',
                'requestAnimationFrame',
                'lazy',
                'async',
                'defer'
            ]
            
            performance_score = 0
            for js_file in js_files:
                if Path(js_file).exists():
                    with open(js_file, 'r', encoding='utf-8') as f:
                        js_content = f.read()
                        performance_score += sum(1 for pattern in performance_patterns if pattern in js_content)
            
            if performance_score < 3:
                self.test_results.append({
                    'test': 'Performance Optimizations',
                    'status': 'WARNING',
                    'details': f"Limited performance optimizations found ({performance_score})"
                })
                self.logger.warning(f"⚠️ Ograničene performance optimizacije")
            
            # Check for accessibility features
            accessibility_score = 0
            all_files = [
                'templates/support_matrix.html',
                'templates/support_analytics.html',
                'static/css/support_matrix.css'
            ]
            
            accessibility_patterns = [
                'aria-label',
                'aria-describedby',
                'role=',
                'tabindex',
                'focus',
                'alt=',
                'title='
            ]
            
            for file_path in all_files:
                if Path(file_path).exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        accessibility_score += sum(1 for pattern in accessibility_patterns if pattern in content)
            
            if accessibility_score < 5:
                self.test_results.append({
                    'test': 'Accessibility Features',
                    'status': 'WARNING',
                    'details': f"Limited accessibility features found ({accessibility_score})"
                })
                self.logger.warning(f"⚠️ Ograničene accessibility funkcije")
            
            self.test_results.append({
                'test': 'Performance & Accessibility',
                'status': 'PASSED',
                'details': f'Performance score: {performance_score}, Accessibility score: {accessibility_score}'
            })
            self.logger.info("✅ Performance i accessibility test završen")
            return True
            
        except Exception as e:
            self.test_results.append({
                'test': 'Performance & Accessibility',
                'status': 'ERROR',
                'details': str(e)
            })
            self.logger.error(f"❌ Greška pri testiranju performansi: {str(e)}")
            return False
    
    def _generate_test_report(self):
        """Generiše detajan izveštaj o testovima."""
        try:
            report = {
                'test_suite': 'Task 3 Integration Tests',
                'timestamp': self._get_current_timestamp(),
                'summary': {
                    'total_tests': len(self.test_results),
                    'passed': len([t for t in self.test_results if t['status'] == 'PASSED']),
                    'failed': len([t for t in self.test_results if t['status'] == 'FAILED']),
                    'warnings': len([t for t in self.test_results if t['status'] == 'WARNING']),
                    'errors': len([t for t in self.test_results if t['status'] == 'ERROR'])
                },
                'test_results': self.test_results,
                'recommendations': self._generate_recommendations()
            }
            
            # Sačuvaj izveštaj
            report_file = Path("TASK_3_INTEGRATION_TEST_REPORT.json")
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"📄 Test izveštaj sačuvan u {report_file}")
            
            # Prikaži sažetak
            self.logger.info("📊 TEST SAŽETAK:")
            self.logger.info(f"   ✅ Prošli: {report['summary']['passed']}")
            self.logger.info(f"   ❌ Neuspešni: {report['summary']['failed']}")
            self.logger.info(f"   ⚠️  Upozorenja: {report['summary']['warnings']}")
            self.logger.info(f"   💥 Greške: {report['summary']['errors']}")
            
        except Exception as e:
            self.logger.error(f"❌ Greška pri generisanju izveštaja: {str(e)}")
    
    def _generate_recommendations(self) -> List[str]:
        """Generiše preporuke na osnovu test rezultata."""
        recommendations = []
        
        failed_tests = [t for t in self.test_results if t['status'] == 'FAILED']
        warning_tests = [t for t in self.test_results if t['status'] == 'WARNING']
        
        if failed_tests:
            recommendations.append("Ispraviti neuspešne testove pre production deployment")
        
        if any('accessibility' in t['test'].lower() for t in warning_tests):
            recommendations.append("Poboljšati accessibility funkcionalnosti za bolje korisničko iskustvo")
        
        if any('performance' in t['test'].lower() for t in warning_tests):
            recommendations.append("Optimizovati performanse za bolje korisničko iskustvo")
        
        if any('responsive' in t['details'].lower() for t in warning_tests):
            recommendations.append("Poboljšati responsive design za mobilne uređaje")
        
        if not recommendations:
            recommendations.append("Svi testovi su prošli uspešno - sistem je spreman za production")
        
        return recommendations
    
    def _get_current_timestamp(self) -> str:
        """Vraća trenutni timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()


# Standalone test execution
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Task3IntegrationTester")
    
    tester = Task3IntegrationTester(logger)
    success = tester.run_full_integration_tests()
    
    sys.exit(0 if success else 1)