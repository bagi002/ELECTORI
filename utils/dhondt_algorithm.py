"""
D'Hondt Algorithm implementation for ELECTORI application.
Provides seat allocation methods for parliamentary elections.
"""

from typing import Dict, List, Tuple, Optional
import math


class DHondtCalculator:
    """Implementation of the D'Hondt method for proportional representation."""
    
    def __init__(self, results: Dict[str, float], total_seats: int, threshold: float = 0.0):
        """
        Initialize D'Hondt calculator.
        
        Args:
            results: Dictionary mapping party/candidacy names to vote percentages
            total_seats: Total number of seats to allocate
            threshold: Electoral threshold (percentage) for seat eligibility
        """
        self.results = results
        self.total_seats = total_seats
        self.threshold = threshold
        self.eligible_parties = self._filter_eligible_parties()
        
    def _filter_eligible_parties(self) -> Dict[str, float]:
        """Filter parties that meet the electoral threshold."""
        return {
            party: percentage 
            for party, percentage in self.results.items() 
            if percentage >= self.threshold
        }
    
    def calculate_seats(self) -> Dict[str, int]:
        """
        Calculate seat allocation using D'Hondt method.
        
        Returns:
            Dictionary mapping party names to seat counts
        """
        if not self.eligible_parties:
            return {}
        
        # Initialize seats for all eligible parties
        seats = {party: 0 for party in self.eligible_parties.keys()}
        
        # Allocate seats one by one
        for _ in range(self.total_seats):
            # Calculate quotients for each party
            quotients = {}
            for party, percentage in self.eligible_parties.items():
                # D'Hondt quotient = votes / (seats + 1)
                quotient = percentage / (seats[party] + 1)
                quotients[party] = quotient
            
            # Award seat to party with highest quotient
            winner = max(quotients.items(), key=lambda x: x[1])[0]
            seats[winner] += 1
        
        return seats
    
    def calculate_detailed_allocation(self) -> Dict:
        """
        Calculate detailed seat allocation with step-by-step breakdown.
        
        Returns:
            Detailed allocation information including quotients and allocation steps
        """
        if not self.eligible_parties:
            return {
                'seats': {},
                'steps': [],
                'summary': {
                    'total_seats': self.total_seats,
                    'eligible_parties': 0,
                    'threshold': self.threshold
                }
            }
        
        seats = {party: 0 for party in self.eligible_parties.keys()}
        allocation_steps = []
        
        # Track allocation step by step
        for seat_number in range(1, self.total_seats + 1):
            quotients = {}
            for party, percentage in self.eligible_parties.items():
                quotient = percentage / (seats[party] + 1)
                quotients[party] = quotient
            
            # Find winner
            winner = max(quotients.items(), key=lambda x: x[1])
            winner_party = winner[0]
            winner_quotient = winner[1]
            
            # Award seat
            seats[winner_party] += 1
            
            # Record step
            step = {
                'seat_number': seat_number,
                'quotients': quotients.copy(),
                'winner': winner_party,
                'winner_quotient': winner_quotient,
                'seats_after': seats.copy()
            }
            allocation_steps.append(step)
        
        # Calculate final statistics
        total_percentage = sum(self.eligible_parties.values())
        seat_percentages = {
            party: (seat_count / self.total_seats * 100) if self.total_seats > 0 else 0
            for party, seat_count in seats.items()
        }
        
        disproportionality = self._calculate_disproportionality(seat_percentages)
        
        return {
            'seats': seats,
            'steps': allocation_steps,
            'summary': {
                'total_seats': self.total_seats,
                'eligible_parties': len(self.eligible_parties),
                'threshold': self.threshold,
                'total_vote_percentage': total_percentage,
                'seat_percentages': seat_percentages,
                'disproportionality_index': disproportionality
            },
            'eligible_parties': self.eligible_parties.copy(),
            'excluded_parties': {
                party: percentage 
                for party, percentage in self.results.items() 
                if percentage < self.threshold
            }
        }
    
    def _calculate_disproportionality(self, seat_percentages: Dict[str, float]) -> float:
        """
        Calculate Gallagher disproportionality index.
        
        Args:
            seat_percentages: Dictionary of seat percentages by party
            
        Returns:
            Disproportionality index (lower is more proportional)
        """
        if not self.eligible_parties:
            return 0.0
        
        squared_differences = 0
        for party in self.eligible_parties.keys():
            vote_percentage = self.eligible_parties[party]
            seat_percentage = seat_percentages.get(party, 0)
            squared_differences += (vote_percentage - seat_percentage) ** 2
        
        return math.sqrt(squared_differences / 2)
    
    def compare_with_pure_proportional(self) -> Dict:
        """
        Compare D'Hondt results with pure proportional allocation.
        
        Returns:
            Comparison showing differences between methods
        """
        dhondt_seats = self.calculate_seats()
        
        # Calculate pure proportional allocation
        proportional_seats = {}
        for party, percentage in self.eligible_parties.items():
            exact_seats = (percentage / 100) * self.total_seats
            proportional_seats[party] = round(exact_seats)
        
        # Adjust for rounding discrepancies
        total_allocated = sum(proportional_seats.values())
        if total_allocated != self.total_seats:
            # Simple adjustment: add/remove seats from largest remainder
            remainders = {
                party: ((percentage / 100) * self.total_seats) - proportional_seats[party]
                for party, percentage in self.eligible_parties.items()
            }
            
            while total_allocated < self.total_seats:
                party_to_increase = max(remainders.items(), key=lambda x: x[1])[0]
                proportional_seats[party_to_increase] += 1
                remainders[party_to_increase] -= 1
                total_allocated += 1
            
            while total_allocated > self.total_seats:
                party_to_decrease = min(remainders.items(), key=lambda x: x[1])[0]
                proportional_seats[party_to_decrease] -= 1
                remainders[party_to_decrease] += 1
                total_allocated -= 1
        
        # Calculate differences
        differences = {}
        for party in self.eligible_parties.keys():
            dhondt_count = dhondt_seats.get(party, 0)
            proportional_count = proportional_seats.get(party, 0)
            differences[party] = dhondt_count - proportional_count
        
        return {
            'dhondt_seats': dhondt_seats,
            'proportional_seats': proportional_seats,
            'differences': differences,
            'summary': {
                'dhondt_favors_large': sum(1 for d in differences.values() if d > 0),
                'dhondt_penalizes_small': sum(1 for d in differences.values() if d < 0),
                'total_difference': sum(abs(d) for d in differences.values())
            }
        }
    
    def simulate_threshold_effects(self, thresholds: List[float] = None) -> Dict:
        """
        Simulate how different electoral thresholds affect seat allocation.
        
        Args:
            thresholds: List of threshold percentages to test
            
        Returns:
            Results for each threshold level
        """
        if thresholds is None:
            thresholds = [0, 1, 2, 3, 4, 5, 10]
        
        threshold_results = {}
        
        for threshold in thresholds:
            calculator = DHondtCalculator(self.results, self.total_seats, threshold)
            allocation = calculator.calculate_detailed_allocation()
            
            threshold_results[threshold] = {
                'seats': allocation['seats'],
                'eligible_parties': len(allocation['eligible_parties']),
                'excluded_parties': len(allocation['excluded_parties']),
                'excluded_vote_percentage': sum(allocation['excluded_parties'].values()),
                'disproportionality': allocation['summary']['disproportionality_index']
            }
        
        return {
            'threshold_analysis': threshold_results,
            'recommendations': self._analyze_threshold_effects(threshold_results)
        }
    
    def _analyze_threshold_effects(self, threshold_results: Dict) -> Dict:
        """Analyze the effects of different thresholds."""
        analysis = {
            'most_proportional': None,
            'least_fragmented': None,
            'balanced_representation': None
        }
        
        # Find most proportional (lowest disproportionality)
        min_disprop = min(
            result['disproportionality'] 
            for result in threshold_results.values()
        )
        analysis['most_proportional'] = next(
            threshold for threshold, result in threshold_results.items()
            if result['disproportionality'] == min_disprop
        )
        
        # Find least fragmented (fewest parties)
        min_parties = min(
            result['eligible_parties'] 
            for result in threshold_results.values()
        )
        analysis['least_fragmented'] = next(
            threshold for threshold, result in threshold_results.items()
            if result['eligible_parties'] == min_parties
        )
        
        # Find balanced (good proportionality with reasonable party count)
        balanced_score = {}
        for threshold, result in threshold_results.items():
            # Simple scoring: penalize high disproportionality and too many/few parties
            party_penalty = abs(result['eligible_parties'] - 5)  # Optimal around 5 parties
            disprop_penalty = result['disproportionality'] * 2
            balanced_score[threshold] = party_penalty + disprop_penalty
        
        analysis['balanced_representation'] = min(
            balanced_score.items(), key=lambda x: x[1]
        )[0]
        
        return analysis


def calculate_parliament_composition(election_results: Dict[int, float], 
                                   total_seats: int = 250, 
                                   threshold: float = 3.0) -> Dict:
    """
    High-level function to calculate parliament composition.
    
    Args:
        election_results: Dictionary mapping candidacy IDs to vote percentages
        total_seats: Total parliamentary seats
        threshold: Electoral threshold percentage
        
    Returns:
        Complete parliament composition analysis
    """
    # Convert candidacy IDs to strings for D'Hondt calculator
    string_results = {str(cid): percentage for cid, percentage in election_results.items()}
    
    calculator = DHondtCalculator(string_results, total_seats, threshold)
    detailed_allocation = calculator.calculate_detailed_allocation()
    comparison = calculator.compare_with_pure_proportional()
    threshold_analysis = calculator.simulate_threshold_effects()
    
    # Convert string keys back to integers
    seats = {int(k): v for k, v in detailed_allocation['seats'].items()}
    
    return {
        'seats': seats,
        'allocation_details': detailed_allocation,
        'proportionality_comparison': comparison,
        'threshold_analysis': threshold_analysis,
        'parliament_stats': {
            'total_seats': total_seats,
            'threshold_used': threshold,
            'parties_in_parliament': len(seats),
            'government_threshold': total_seats // 2 + 1,
            'qualified_majority_threshold': int(total_seats * 2/3)
        }
    }


def find_coalition_majorities(seats: Dict[int, int], 
                            total_seats: int, 
                            majority_type: str = 'simple') -> List[List[int]]:
    """
    Find all possible coalition combinations that achieve majority.
    
    Args:
        seats: Dictionary mapping candidacy/party IDs to seat counts
        total_seats: Total number of parliamentary seats
        majority_type: 'simple' (50%+1) or 'qualified' (2/3)
        
    Returns:
        List of coalition combinations (each as list of party IDs)
    """
    if majority_type == 'qualified':
        required_seats = int(total_seats * 2/3)
    else:
        required_seats = total_seats // 2 + 1
    
    parties = list(seats.keys())
    coalitions = []
    
    # Generate all possible combinations
    from itertools import combinations
    
    for r in range(1, len(parties) + 1):
        for combo in combinations(parties, r):
            coalition_seats = sum(seats[party] for party in combo)
            if coalition_seats >= required_seats:
                coalitions.append(list(combo))
    
    # Sort by coalition size (smaller coalitions first)
    coalitions.sort(key=len)
    
    return coalitions