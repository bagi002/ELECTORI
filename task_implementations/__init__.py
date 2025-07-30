"""
Base class for task implementations.
"""

import logging
import subprocess
import shutil
from pathlib import Path
from typing import List, Optional
from abc import ABC, abstractmethod

class BaseTaskImplementation(ABC):
    """Bazna klasa za implementacije taskova."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.project_root = Path(__file__).parent.parent.absolute()
        self.templates_dir = self.project_root / "templates"
        self.static_dir = self.project_root / "static"
    
    @abstractmethod
    def execute(self) -> bool:
        """Izvršava implementaciju taska."""
        pass
    
    def create_file(self, file_path: Path, content: str) -> bool:
        """Kreira fajl sa zadatim sadržajem."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.info(f"Kreiran fajl: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Greška pri kreiranju fajla {file_path}: {e}")
            return False
    
    def backup_file(self, file_path: Path) -> bool:
        """Pravi backup postojećeg fajla."""
        if file_path.exists():
            backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")
            try:
                shutil.copy2(file_path, backup_path)
                self.logger.info(f"Napravljen backup: {backup_path}")
                return True
            except Exception as e:
                self.logger.error(f"Greška pri backup-u {file_path}: {e}")
                return False
        return True
    
    def run_tests(self, test_pattern: str = None) -> bool:
        """Pokreće testove."""
        try:
            cmd = ["python", "-m", "pytest", "-v"]
            if test_pattern:
                cmd.extend(["-k", test_pattern])
            
            result = subprocess.run(
                cmd, 
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info("Testovi uspešno prošli")
                return True
            else:
                self.logger.error(f"Testovi neuspešni: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Greška pri pokretanju testova: {e}")
            return False
    
    def validate_html(self, html_content: str) -> bool:
        """Osnovne validacije HTML-a."""
        # Check if it's a template that extends another template
        if '{% extends' in html_content:
            # Template validation - check for basic block structure
            required_elements = ['{% block', '{% endblock']
            for element in required_elements:
                if element not in html_content:
                    self.logger.warning(f"Template ne sadrži obavezni element: {element}")
                    return False
        else:
            # Full HTML page validation
            required_tags = ['<!DOCTYPE html>', '<html', '<head>', '<body>']
            for tag in required_tags:
                if tag not in html_content:
                    self.logger.warning(f"HTML ne sadrži obavezni tag: {tag}")
                    return False
        return True
    
    def validate_css(self, css_content: str) -> bool:
        """Osnovne validacije CSS-a."""
        # Jednostavna validacija da CSS sadrži osnovne selektore
        if not css_content.strip():
            self.logger.warning("CSS fajl je prazan")
            return False
        return True
    
    def validate_js(self, js_content: str) -> bool:
        """Osnovne validacije JavaScript-a."""
        # Jednostavna sintaksna proverava
        try:
            # Osnovne provere za syntax greške
            if 'function' not in js_content and '=>' not in js_content and 'const' not in js_content:
                self.logger.warning("JavaScript fajl ne sadrži funkcije ili varijable")
                return False
            return True
        except Exception as e:
            self.logger.error(f"Greška pri validaciji JS: {e}")
            return False