#!/usr/bin/env python3
"""
ELECTORI Task Agent - Automated Task Execution System

Agent koji automatski izvršava TASK 2 iz fajla DEVELOPMENT_TASKS.md.
Omogućava sekvencijalno izvršavanje pod-taskova sa testiranjem i praćenjem progresije.
"""

import json
import sys
import argparse
import logging
import traceback
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class SubTask:
    """Reprezentuje jedan pod-task."""
    id: str
    name: str
    description: str
    estimated_time: int  # u minutima
    dependencies: List[str]
    status: TaskStatus = TaskStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error_message: Optional[str] = None

@dataclass
class Task:
    """Reprezentuje glavni task sa pod-taskovima."""
    id: str
    name: str
    description: str
    sub_tasks: List[SubTask]
    status: TaskStatus = TaskStatus.PENDING

class TaskProgress:
    """Klasa za čuvanje i učitavanje progresije taskova."""
    
    def __init__(self, progress_file: str = "task_progress.json"):
        self.progress_file = Path(progress_file)
        self.progress_data: Dict[str, Any] = {}
        self.load_progress()
    
    def load_progress(self):
        """Učitava progresiju iz fajla."""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    self.progress_data = json.load(f)
            except Exception as e:
                logging.warning(f"Greška pri učitavanju progresije: {e}")
                self.progress_data = {}
    
    def save_progress(self):
        """Čuva progresiju u fajl."""
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.progress_data, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            logging.error(f"Greška pri čuvanju progresije: {e}")
    
    def update_task_status(self, task_id: str, sub_task_id: str, status: TaskStatus, 
                          error_message: Optional[str] = None):
        """Ažurira status pod-taska."""
        if task_id not in self.progress_data:
            self.progress_data[task_id] = {}
        
        self.progress_data[task_id][sub_task_id] = {
            'status': status.value,
            'timestamp': datetime.now().isoformat(),
            'error_message': error_message
        }
        self.save_progress()
    
    def get_task_status(self, task_id: str, sub_task_id: str) -> TaskStatus:
        """Vraća status pod-taska."""
        if task_id in self.progress_data and sub_task_id in self.progress_data[task_id]:
            status_str = self.progress_data[task_id][sub_task_id]['status']
            return TaskStatus(status_str)
        return TaskStatus.PENDING

class TaskAgent:
    """Glavni agent za izvršavanje taskova."""
    
    def __init__(self, progress_file: str = "task_progress.json"):
        self.progress = TaskProgress(progress_file)
        self.logger = self._setup_logger()
        self.task_2 = self._define_task_2()
    
    def _setup_logger(self) -> logging.Logger:
        """Postavlja logger."""
        logger = logging.getLogger("TaskAgent")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _define_task_2(self) -> Task:
        """Definiše TASK 2 sa pod-taskovima."""
        sub_tasks = [
            SubTask(
                id="task_2_1",
                name="Frontend Framework i Layout",
                description="Kreiranje osnovnog frontend-a sa HTML templates, CSS styling, JavaScript modules",
                estimated_time=90,
                dependencies=[]
            ),
            SubTask(
                id="task_2_2", 
                name="Simulation Management UI",
                description="Kompletna funkcionalnost za upravljanje simulacijama",
                estimated_time=75,
                dependencies=["task_2_1"]
            ),
            SubTask(
                id="task_2_3",
                name="City Management System", 
                description="Kompletno upravljanje gradovima",
                estimated_time=60,
                dependencies=["task_2_2"]
            ),
            SubTask(
                id="task_2_4",
                name="Party Management System",
                description="Kompletan sistem za upravljanje partijama", 
                estimated_time=90,
                dependencies=["task_2_3"]
            )
        ]
        
        return Task(
            id="task_2",
            name="FAZA 2: OSNOVNA FUNKCIONALNOST", 
            description="Kreiranje osnovnih frontend funkcionalnosti za ELECTORI aplikaciju",
            sub_tasks=sub_tasks
        )
    
    def run_task(self, task_id: str, force_restart: bool = False) -> bool:
        """Pokreće izvršavanje taska."""
        if task_id != "task_2":
            self.logger.error(f"Nepoznat task ID: {task_id}")
            return False
        
        self.logger.info(f"Pokretanje {self.task_2.name}")
        self.logger.info(f"Opis: {self.task_2.description}")
        
        success = True
        for sub_task in self.task_2.sub_tasks:
            if not force_restart:
                current_status = self.progress.get_task_status(task_id, sub_task.id)
                if current_status == TaskStatus.COMPLETED:
                    self.logger.info(f"Pod-task {sub_task.id} već je završen, preskačem")
                    continue
            
            # Proveri zavisnosti
            if not self._check_dependencies(task_id, sub_task):
                self.logger.error(f"Zavisnosti za {sub_task.id} nisu ispunjene")
                success = False
                break
            
            # Izvršava pod-task
            if not self._execute_sub_task(task_id, sub_task):
                success = False
                break
        
        if success:
            self.logger.info(f"Task {task_id} uspešno završen!")
            self._run_integration_tests(task_id)
        else:
            self.logger.error(f"Task {task_id} nije uspešno završen")
        
        return success
    
    def _check_dependencies(self, task_id: str, sub_task: SubTask) -> bool:
        """Proverava da li su zavisnosti za pod-task ispunjene."""
        for dep_id in sub_task.dependencies:
            dep_status = self.progress.get_task_status(task_id, dep_id)
            if dep_status != TaskStatus.COMPLETED:
                self.logger.error(f"Zavisnost {dep_id} nije završena za {sub_task.id}")
                return False
        return True
    
    def _execute_sub_task(self, task_id: str, sub_task: SubTask) -> bool:
        """Izvršava pojedinačan pod-task."""
        self.logger.info(f"Pokretanje pod-taska: {sub_task.name}")
        self.logger.info(f"Procenjeno vreme: {sub_task.estimated_time} minuta")
        
        # Označava početak
        self.progress.update_task_status(task_id, sub_task.id, TaskStatus.RUNNING)
        
        try:
            # Poziva specifičnu metodu za pod-task
            method_name = f"_execute_{sub_task.id}"
            if hasattr(self, method_name):
                method = getattr(self, method_name)
                success = method()
                
                if success:
                    self.progress.update_task_status(task_id, sub_task.id, TaskStatus.COMPLETED)
                    self.logger.info(f"Pod-task {sub_task.id} uspešno završen")
                else:
                    self.progress.update_task_status(task_id, sub_task.id, TaskStatus.FAILED, 
                                                   "Izvršavanje neuspešno")
                    self.logger.error(f"Pod-task {sub_task.id} neuspešan")
                
                return success
            else:
                error_msg = f"Metoda {method_name} nije implementirana"
                self.progress.update_task_status(task_id, sub_task.id, TaskStatus.FAILED, error_msg)
                self.logger.error(error_msg)
                return False
                
        except Exception as e:
            error_msg = f"Greška pri izvršavanju {sub_task.id}: {str(e)}"
            self.progress.update_task_status(task_id, sub_task.id, TaskStatus.FAILED, error_msg)
            self.logger.error(error_msg)
            self.logger.debug(traceback.format_exc())
            return False
    
    def _execute_task_2_1(self) -> bool:
        """Izvršava Task 2.1: Frontend Framework i Layout."""
        self.logger.info("Implementiranje Frontend Framework i Layout...")
        
        from task_implementations.task_2_1_frontend import FrontendImplementation
        impl = FrontendImplementation(self.logger)
        return impl.execute()
    
    def _execute_task_2_2(self) -> bool:
        """Izvršava Task 2.2: Simulation Management UI."""
        self.logger.info("Implementiranje Simulation Management UI...")
        
        from task_implementations.task_2_2_simulation import SimulationManagementImplementation
        impl = SimulationManagementImplementation(self.logger)
        return impl.execute()
    
    def _execute_task_2_3(self) -> bool:
        """Izvršava Task 2.3: City Management System."""
        self.logger.info("Implementiranje City Management System...")
        
        from task_implementations.task_2_3_city import CityManagementImplementation
        impl = CityManagementImplementation(self.logger)
        return impl.execute()
    
    def _execute_task_2_4(self) -> bool:
        """Izvršava Task 2.4: Party Management System."""
        self.logger.info("Implementiranje Party Management System...")
        
        from task_implementations.task_2_4_party import PartyManagementImplementation
        impl = PartyManagementImplementation(self.logger)
        return impl.execute()
    
    def _run_integration_tests(self, task_id: str):
        """Pokreće integracione testove za kompletan task."""
        self.logger.info(f"Pokretanje integracionih testova za {task_id}")
        
        # Implementirati integracione testove
        from task_implementations.integration_tests import IntegrationTester
        tester = IntegrationTester(self.logger)
        tester.run_task_2_integration_tests()
    
    def show_progress(self, task_id: str = "task_2"):
        """Prikazuje trenutnu progresiju taska."""
        print(f"\n=== Progresija za {self.task_2.name} ===\n")
        
        for sub_task in self.task_2.sub_tasks:
            status = self.progress.get_task_status(task_id, sub_task.id)
            status_icon = {
                TaskStatus.PENDING: "⏳",
                TaskStatus.RUNNING: "🔄", 
                TaskStatus.COMPLETED: "✅",
                TaskStatus.FAILED: "❌",
                TaskStatus.SKIPPED: "⏭️"
            }.get(status, "❓")
            
            print(f"{status_icon} {sub_task.name}")
            print(f"   Status: {status.value}")
            print(f"   Vreme: {sub_task.estimated_time} min")
            print(f"   Opis: {sub_task.description}")
            
            if task_id in self.progress.progress_data and sub_task.id in self.progress.progress_data[task_id]:
                task_data = self.progress.progress_data[task_id][sub_task.id]
                if 'timestamp' in task_data:
                    print(f"   Poslednja izmena: {task_data['timestamp']}")
                if task_data.get('error_message'):
                    print(f"   Greška: {task_data['error_message']}")
            print()
    
    def reset_progress(self, task_id: str = "task_2", sub_task_id: Optional[str] = None):
        """Resetuje progresiju za task ili pod-task."""
        if sub_task_id:
            if task_id in self.progress.progress_data and sub_task_id in self.progress.progress_data[task_id]:
                del self.progress.progress_data[task_id][sub_task_id]
                self.progress.save_progress()
                self.logger.info(f"Resetovana progresija za {sub_task_id}")
        else:
            if task_id in self.progress.progress_data:
                del self.progress.progress_data[task_id]
                self.progress.save_progress()
                self.logger.info(f"Resetovana progresija za {task_id}")

def main():
    """Glavna funkcija CLI interfejsa."""
    parser = argparse.ArgumentParser(
        description="ELECTORI Task Agent - Automatsko izvršavanje razvojnih taskova"
    )
    parser.add_argument(
        "action", 
        choices=["run", "progress", "reset", "help"],
        help="Akcija koju treba izvršiti"
    )
    parser.add_argument(
        "--task", 
        default="task_2",
        help="ID taska koji se izvršava (default: task_2)"
    )
    parser.add_argument(
        "--sub-task",
        help="ID pod-taska za reset ili pojedinačno pokretanje"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Prisiljava ponovno pokretanje završenih taskova"
    )
    parser.add_argument(
        "--progress-file",
        default="task_progress.json",
        help="Fajl za čuvanje progresije"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Detaljno logovanje"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger("TaskAgent").setLevel(logging.DEBUG)
    
    agent = TaskAgent(args.progress_file)
    
    if args.action == "run":
        success = agent.run_task(args.task, args.force)
        sys.exit(0 if success else 1)
    elif args.action == "progress":
        agent.show_progress(args.task)
    elif args.action == "reset":
        agent.reset_progress(args.task, args.sub_task)
    elif args.action == "help":
        parser.print_help()
        print("\nPrimeri upotrebe:")
        print("  python task_agent.py run                 # Pokreće Task 2")
        print("  python task_agent.py progress            # Prikazuje progresiju")
        print("  python task_agent.py run --force         # Forsirani restart")
        print("  python task_agent.py reset --sub-task task_2_1  # Reset pod-taska")

if __name__ == "__main__":
    main()