"""
Fault Code Parser for HALog Application
Parses fault.txt file into searchable structure
Developer: Tanmay Pandey
Company: gobioeng.com
"""

import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class FaultCodeParser:
    """Parser for LINAC fault codes from fault.txt file"""
    
    def __init__(self, fault_file_path: Optional[str] = None):
        """Initialize the fault code parser"""
        if fault_file_path is None:
            # Default to data/Fault.txt relative to script location
            script_dir = Path(__file__).parent
            fault_file_path = script_dir / "data" / "Fault.txt"
        
        self.fault_file_path = Path(fault_file_path)
        self.fault_codes: Dict[str, Dict[str, str]] = {}
        self.load_fault_codes()
    
    def load_fault_codes(self) -> None:
        """Load fault codes from the fault file"""
        try:
            if not self.fault_file_path.exists():
                print(f"Warning: Fault file not found at {self.fault_file_path}")
                return
            
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            lines = None
            
            for encoding in encodings:
                try:
                    with open(self.fault_file_path, 'r', encoding=encoding) as file:
                        lines = file.readlines()
                    print(f"Successfully read file with {encoding} encoding")
                    break
                except UnicodeDecodeError:
                    continue
            
            if lines is None:
                print(f"Error: Could not read fault file with any supported encoding")
                return
            
            # Skip header line if it exists
            start_line = 1 if lines and ('ID' in lines[0] and 'Description' in lines[0]) else 0
            
            for line_num, line in enumerate(lines[start_line:], start=start_line + 1):
                line = line.strip()
                if not line:
                    continue
                
                # Parse line format: ID\tDescription\tType
                parts = line.split('\t')
                if len(parts) >= 2:
                    fault_id = parts[0].strip()
                    description = parts[1].strip()
                    fault_type = parts[2].strip() if len(parts) > 2 else "Unknown"
                    
                    self.fault_codes[fault_id] = {
                        'description': description,
                        'type': fault_type,
                        'line_number': line_num
                    }
            
            print(f"✓ Loaded {len(self.fault_codes)} fault codes from {self.fault_file_path}")
            
        except Exception as e:
            print(f"Error loading fault codes: {e}")
            self.fault_codes = {}
    
    def search_fault_code(self, code: str) -> Optional[Dict[str, str]]:
        """Search for a specific fault code"""
        code = code.strip()
        if code in self.fault_codes:
            return self.fault_codes[code]
        return None
    
    def search_description(self, search_term: str) -> List[Tuple[str, Dict[str, str]]]:
        """Search fault codes by description keyword"""
        search_term = search_term.lower().strip()
        results = []
        
        for fault_id, fault_data in self.fault_codes.items():
            if search_term in fault_data['description'].lower():
                results.append((fault_id, fault_data))
        
        return results
    
    def get_all_fault_codes(self) -> Dict[str, Dict[str, str]]:
        """Get all fault codes"""
        return self.fault_codes.copy()
    
    def get_fault_types(self) -> List[str]:
        """Get all unique fault types"""
        types = set()
        for fault_data in self.fault_codes.values():
            types.add(fault_data.get('type', 'Unknown'))
        return sorted(list(types))
    
    def get_stats(self) -> Dict[str, int]:
        """Get statistics about loaded fault codes"""
        stats = {
            'total_codes': len(self.fault_codes),
            'types': len(self.get_fault_types())
        }
        
        type_counts = {}
        for fault_data in self.fault_codes.values():
            fault_type = fault_data.get('type', 'Unknown')
            type_counts[fault_type] = type_counts.get(fault_type, 0) + 1
        
        stats['type_breakdown'] = type_counts
        return stats


def test_fault_parser():
    """Test function for the fault code parser"""
    parser = FaultCodeParser()
    stats = parser.get_stats()
    print(f"Fault Code Parser Test:")
    print(f"Total codes: {stats['total_codes']}")
    print(f"Types: {stats['types']}")
    print(f"Type breakdown: {stats['type_breakdown']}")
    
    # Test search
    test_code = "400027"
    result = parser.search_fault_code(test_code)
    if result:
        print(f"\nTest search for {test_code}:")
        print(f"Description: {result['description']}")
        print(f"Type: {result['type']}")
    else:
        print(f"\nCode {test_code} not found")


if __name__ == "__main__":
    test_fault_parser()