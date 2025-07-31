"""
Election Algorithm utilities for ELECTORI application.
Handles election result calculations, vote distribution, and seat allocation.
"""

import random
from typing import Dict, List, Tuple, Optional
from models.election import Election, Candidacy, CandidacyMembership, ElectionResult, ElectionType
from models.party import PartySupport
from models.city import City
from extensions import db


class ElectionCalculator:
    """Main class for election calculations and simulations."""
    
    def __init__(self, election_id: int):
        self.election = Election.get_by_id(election_id)
        if not self.election:
            raise ValueError(f"Election with ID {election_id} not found")
        
        self.cities = City.get_by_simulation(self.election.simulation_id)
        self.candidacies = self.election.candidacies
        
    def calculate_election_results(self, randomness_factor: float = 0.1) -> Dict:
        """
        Calculate election results for all cities and candidacies.
        
        Args:
            randomness_factor: Random variation factor (0.05-0.15 recommended)
            
        Returns:
            Dictionary with election results per city and overall
        """
        results = {
            'election_id': self.election.id,
            'cities': {},
            'national': {},
            'metadata': {
                'total_voters': 0,
                'total_votes': 0,
                'turnout_percentage': 0.0,
                'randomness_factor': randomness_factor
            }
        }
        
        national_totals = {}
        total_population = 0
        total_voters = 0
        
        # Calculate results for each city
        for city in self.cities:
            city_results = self._calculate_city_results(city, randomness_factor)
            results['cities'][city.id] = city_results
            
            # Accumulate national totals
            total_population += city.population
            city_voters = int(city.population * city_results['turnout'] / 100)
            total_voters += city_voters
            
            for candidacy_id, votes in city_results['votes'].items():
                if candidacy_id not in national_totals:
                    national_totals[candidacy_id] = 0
                national_totals[candidacy_id] += votes
        
        # Calculate national percentages
        total_votes = sum(national_totals.values())
        national_percentages = {}
        
        for candidacy_id, votes in national_totals.items():
            percentage = (votes / total_votes * 100) if total_votes > 0 else 0
            national_percentages[candidacy_id] = percentage
        
        results['national'] = {
            'votes': national_totals,
            'percentages': national_percentages,
            'total_votes': total_votes
        }
        
        # Calculate seats if parliamentary election
        if self.election.type == ElectionType.PARLIAMENTARY:
            seats = self._calculate_seats_dhondt(
                national_percentages, 
                total_seats=250,  # Default parliament size
                census_threshold=self.election.census_threshold or 0
            )
            results['national']['seats'] = seats
        
        # Update metadata
        results['metadata'].update({
            'total_voters': total_voters,
            'total_votes': total_votes,
            'turnout_percentage': (total_voters / total_population * 100) if total_population > 0 else 0
        })
        
        return results
    
    def _calculate_city_results(self, city: City, randomness_factor: float) -> Dict:
        """Calculate election results for a specific city."""
        # Get base support for each candidacy
        candidacy_support = {}
        
        for candidacy in self.candidacies:
            base_support = self._get_candidacy_support(candidacy, city)
            candidacy_support[candidacy.id] = base_support
        
        # Apply randomness factor
        randomized_support = self._apply_randomness(candidacy_support, randomness_factor)
        
        # Normalize to 100%
        normalized_support = self._normalize_support(randomized_support)
        
        # Calculate voter turnout (60-85% typical range)
        turnout = random.uniform(60, 85)
        voters = int(city.population * turnout / 100)
        
        # Calculate votes
        votes = {}
        for candidacy_id, percentage in normalized_support.items():
            vote_count = int(voters * percentage / 100)
            votes[candidacy_id] = vote_count
        
        return {
            'city_id': city.id,
            'city_name': city.name,
            'population': city.population,
            'turnout': turnout,
            'voters': voters,
            'votes': votes,
            'percentages': normalized_support
        }
    
    def _get_candidacy_support(self, candidacy: Candidacy, city: City) -> float:
        """Get base support percentage for a candidacy in a city."""
        total_support = 0.0
        
        # Get support from all parties in the candidacy
        for membership in candidacy.memberships:
            party_support = PartySupport.query.filter_by(
                party_id=membership.party_id,
                city_id=city.id
            ).first()
            
            if party_support:
                # Lead party gets full support, other parties get reduced support
                multiplier = 1.0 if membership.is_lead_party else 0.7
                total_support += party_support.support_percentage * multiplier
        
        return min(total_support, 100.0)  # Cap at 100%
    
    def _apply_randomness(self, support_dict: Dict[int, float], factor: float) -> Dict[int, float]:
        """Apply random variation to support percentages."""
        randomized = {}
        
        for candidacy_id, support in support_dict.items():
            # Apply random factor (-factor to +factor)
            variation = random.uniform(-factor, factor) * 100
            new_support = max(0, support + variation)
            randomized[candidacy_id] = new_support
        
        return randomized
    
    def _normalize_support(self, support_dict: Dict[int, float]) -> Dict[int, float]:
        """Normalize support percentages to sum to 100%."""
        total = sum(support_dict.values())
        
        if total == 0:
            # Equal distribution if no support data
            equal_share = 100.0 / len(support_dict)
            return {cid: equal_share for cid in support_dict.keys()}
        
        normalized = {}
        for candidacy_id, support in support_dict.items():
            normalized[candidacy_id] = (support / total) * 100
        
        return normalized
    
    def _calculate_seats_dhondt(self, percentages: Dict[int, float], total_seats: int, census_threshold: float = 0) -> Dict[int, int]:
        """
        Calculate seat allocation using D'Hondt method.
        
        Args:
            percentages: Vote percentages by candidacy
            total_seats: Total number of seats to allocate
            census_threshold: Minimum percentage needed to win seats
            
        Returns:
            Dictionary with seat counts by candidacy
        """
        # Filter candidacies above census threshold
        eligible = {
            cid: pct for cid, pct in percentages.items() 
            if pct >= census_threshold
        }
        
        if not eligible:
            return {}
        
        # Initialize seats
        seats = {candidacy_id: 0 for candidacy_id in eligible.keys()}
        
        # D'Hondt allocation
        for _ in range(total_seats):
            # Calculate quotients for each candidacy
            quotients = {}
            for candidacy_id, percentage in eligible.items():
                quotient = percentage / (seats[candidacy_id] + 1)
                quotients[candidacy_id] = quotient
            
            # Award seat to candidacy with highest quotient
            winner = max(quotients.items(), key=lambda x: x[1])[0]
            seats[winner] += 1
        
        return seats
    
    def save_results_to_database(self, results: Dict) -> None:
        """Save calculated results to the database."""
        try:
            # Clear existing results for this election
            ElectionResult.query.filter_by(election_id=self.election.id).delete()
            
            # Save city results
            for city_id, city_data in results['cities'].items():
                for candidacy_id, votes in city_data['votes'].items():
                    percentage = city_data['percentages'][candidacy_id]
                    
                    result = ElectionResult.create(
                        election_id=self.election.id,
                        candidacy_id=candidacy_id,
                        city_id=city_id,
                        votes_count=votes,
                        vote_percentage=percentage
                    )
            
            # Save national results (for parliamentary elections with seats)
            if 'seats' in results['national']:
                for candidacy_id, votes in results['national']['votes'].items():
                    percentage = results['national']['percentages'][candidacy_id]
                    seats = results['national']['seats'].get(candidacy_id, 0)
                    
                    result = ElectionResult.create(
                        election_id=self.election.id,
                        candidacy_id=candidacy_id,
                        city_id=None,  # National result
                        votes_count=votes,
                        vote_percentage=percentage,
                        seats_won=seats
                    )
            
            # Update election status
            self.election.update(status='completed')
            
        except Exception as e:
            db.session.rollback()
            raise e


class PresidentialElectionCalculator(ElectionCalculator):
    """Specialized calculator for presidential elections with runoff capability."""
    
    def calculate_presidential_results(self, support_decisions: Dict[int, int] = None) -> Dict:
        """
        Calculate presidential election results.
        
        Args:
            support_decisions: For second round, which candidate each eliminated party supports
            
        Returns:
            Election results with potential runoff information
        """
        if self.election.round_number == 1:
            return self._calculate_first_round()
        else:
            return self._calculate_second_round(support_decisions or {})
    
    def _calculate_first_round(self) -> Dict:
        """Calculate first round of presidential election."""
        results = self.calculate_election_results(randomness_factor=0.08)
        
        # Check if runoff is needed (no candidate above 50%)
        national_percentages = results['national']['percentages']
        max_percentage = max(national_percentages.values()) if national_percentages else 0
        
        runoff_needed = max_percentage < 50.0 and len(national_percentages) > 1
        
        if runoff_needed:
            # Find top 2 candidates
            sorted_candidates = sorted(
                national_percentages.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            top_two = [cid for cid, _ in sorted_candidates[:2]]
            
            results['runoff'] = {
                'needed': True,
                'candidates': top_two,
                'eliminated': [cid for cid, _ in sorted_candidates[2:]]
            }
        else:
            results['runoff'] = {'needed': False}
        
        return results
    
    def _calculate_second_round(self, support_decisions: Dict[int, int]) -> Dict:
        """
        Calculate second round with vote transfers.
        
        Args:
            support_decisions: Which candidate each eliminated party supports
        """
        # Get first round results
        first_round_results = ElectionResult.get_by_election(self.election.id)
        
        # Calculate base support for remaining candidates
        remaining_candidates = []
        for candidacy in self.candidacies:
            if any(r.candidacy_id == candidacy.id for r in first_round_results):
                remaining_candidates.append(candidacy.id)
        
        if len(remaining_candidates) != 2:
            raise ValueError("Second round should have exactly 2 candidates")
        
        # Calculate transfers
        transferred_results = {}
        total_population = sum(city.population for city in self.cities)
        
        for city in self.cities:
            city_results = self._calculate_second_round_city(
                city, remaining_candidates, support_decisions
            )
            transferred_results[city.id] = city_results
        
        # Aggregate national results
        national_totals = {cid: 0 for cid in remaining_candidates}
        total_votes = 0
        
        for city_data in transferred_results.values():
            for candidacy_id, votes in city_data['votes'].items():
                national_totals[candidacy_id] += votes
            total_votes += sum(city_data['votes'].values())
        
        national_percentages = {
            cid: (votes / total_votes * 100) if total_votes > 0 else 0
            for cid, votes in national_totals.items()
        }
        
        return {
            'election_id': self.election.id,
            'round': 2,
            'cities': transferred_results,
            'national': {
                'votes': national_totals,
                'percentages': national_percentages,
                'total_votes': total_votes
            },
            'winner': max(national_percentages.items(), key=lambda x: x[1])[0]
        }
    
    def _calculate_second_round_city(self, city: City, remaining_candidates: List[int], 
                                   support_decisions: Dict[int, int]) -> Dict:
        """Calculate second round results for a city with vote transfers."""
        # Get original support for remaining candidates
        base_support = {}
        for candidacy_id in remaining_candidates:
            candidacy = next(c for c in self.candidacies if c.id == candidacy_id)
            base_support[candidacy_id] = self._get_candidacy_support(candidacy, city)
        
        # Apply vote transfers from eliminated candidates
        for eliminated_id, supported_id in support_decisions.items():
            if supported_id in remaining_candidates:
                eliminated_candidacy = next(c for c in self.candidacies if c.id == eliminated_id)
                eliminated_support = self._get_candidacy_support(eliminated_candidacy, city)
                
                # Transfer 70-90% of eliminated candidate's support
                transfer_rate = random.uniform(0.7, 0.9)
                transferred_support = eliminated_support * transfer_rate
                
                base_support[supported_id] += transferred_support
        
        # Normalize and calculate votes
        normalized = self._normalize_support(base_support)
        turnout = random.uniform(65, 80)  # Slightly higher turnout in runoff
        voters = int(city.population * turnout / 100)
        
        votes = {}
        for candidacy_id, percentage in normalized.items():
            vote_count = int(voters * percentage / 100)
            votes[candidacy_id] = vote_count
        
        return {
            'city_id': city.id,
            'votes': votes,
            'percentages': normalized,
            'turnout': turnout,
            'voters': voters
        }


def simulate_election(election_id: int, randomness_factor: float = 0.1) -> Dict:
    """
    Main function to simulate an election.
    
    Args:
        election_id: ID of the election to simulate
        randomness_factor: Random variation factor
        
    Returns:
        Complete election results
    """
    election = Election.get_by_id(election_id)
    if not election:
        raise ValueError(f"Election with ID {election_id} not found")
    
    if election.type == ElectionType.PRESIDENTIAL:
        calculator = PresidentialElectionCalculator(election_id)
        results = calculator.calculate_presidential_results()
    else:
        calculator = ElectionCalculator(election_id)
        results = calculator.calculate_election_results(randomness_factor)
    
    # Save results to database
    calculator.save_results_to_database(results)
    
    return results


def get_election_statistics(election_id: int) -> Dict:
    """Get comprehensive statistics for an election."""
    election = Election.get_by_id(election_id)
    if not election:
        raise ValueError(f"Election with ID {election_id} not found")
    
    results = ElectionResult.get_by_election(election_id)
    
    stats = {
        'election_id': election_id,
        'total_results': len(results),
        'cities_count': len(set(r.city_id for r in results if r.city_id)),
        'candidacies_count': len(set(r.candidacy_id for r in results)),
        'total_votes': sum(r.votes_count for r in results if r.city_id),  # Only city results
        'national_results': [r for r in results if r.city_id is None]
    }
    
    return stats