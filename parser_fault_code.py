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
    """Parser for LINAC fault codes from multiple fault databases"""
    
    def __init__(self, hal_file_path: Optional[str] = None, tb_file_path: Optional[str] = None):
        """Initialize the fault code parser with multiple databases"""
        script_dir = Path(__file__).parent
        
        if hal_file_path is None:
            hal_file_path = script_dir / "data" / "HALfault.txt"
        if tb_file_path is None:
            tb_file_path = script_dir / "data" / "TBFault.txt"
        
        self.hal_file_path = Path(hal_file_path)
        self.tb_file_path = Path(tb_file_path)
        self.fault_codes: Dict[str, Dict[str, str]] = {}
        self.load_fault_codes()
    
    def load_fault_codes(self) -> None:
        """Load fault codes from both HAL and TB fault files"""
        self.fault_codes = {}
        
        # Load HAL fault codes
        self._load_file(self.hal_file_path, "HAL")
        
        # Load TB fault codes
        self._load_file(self.tb_file_path, "TB")
        
        print(f"✓ Total loaded {len(self.fault_codes)} fault codes from both databases")
    
    def _load_file(self, file_path: Path, database_source: str) -> None:
        """Load fault codes from a single file"""
        try:
            if not file_path.exists():
                print(f"Warning: Fault file not found at {file_path}")
                return
            
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            lines = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        lines = file.readlines()
                    print(f"Successfully read {database_source} file with {encoding} encoding")
                    break
                except UnicodeDecodeError:
                    continue
            
            if lines is None:
                print(f"Error: Could not read {database_source} fault file with any supported encoding")
                return
            
            # Skip header line if it exists
            start_line = 1 if lines and ('ID' in lines[0] and 'Description' in lines[0]) else 0
            codes_loaded = 0
            
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
                    
                    # Store with database source information
                    self.fault_codes[fault_id] = {
                        'description': description,
                        'type': fault_type,
                        'line_number': line_num,
                        'database': database_source,
                        'file_path': str(file_path)
                    }
                    codes_loaded += 1
            
            print(f"✓ Loaded {codes_loaded} fault codes from {database_source} database ({file_path})")
            
        except Exception as e:
            print(f"Error loading {database_source} fault codes: {e}")
    
    def search_fault_code(self, code: str) -> Optional[Dict[str, str]]:
        """Search for a specific fault code in both databases"""
        code = code.strip()
        if code in self.fault_codes:
            result = self.fault_codes[code].copy()
            # Add user-friendly database description
            db = result.get('database', 'Unknown')
            if db == 'HAL':
                result['database_description'] = 'HAL Description'
            elif db == 'TB':
                result['database_description'] = 'TB Description'
            else:
                result['database_description'] = 'NA'
            return result
        return None
    
    def get_stats(self) -> Dict[str, int]:
        """Get statistics about loaded fault codes from both databases"""
        stats = {
            'total_codes': len(self.fault_codes),
            'types': len(self.get_fault_types())
        }
        
        # Count by database
        hal_count = sum(1 for data in self.fault_codes.values() if data.get('database') == 'HAL')
        tb_count = sum(1 for data in self.fault_codes.values() if data.get('database') == 'TB')
        
        stats['hal_codes'] = hal_count
        stats['tb_codes'] = tb_count
        
        # Count by type
        type_counts = {}
        for fault_data in self.fault_codes.values():
            fault_type = fault_data.get('type', 'Unknown')
            type_counts[fault_type] = type_counts.get(fault_type, 0) + 1
        
        stats['type_breakdown'] = type_counts
        return stats
    
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
        """Get statistics about loaded fault codes from both databases"""
        stats = {
            'total_codes': len(self.fault_codes),
            'types': len(self.get_fault_types())
        }
        
        # Count by database
        hal_count = sum(1 for data in self.fault_codes.values() if data.get('database') == 'HAL')
        tb_count = sum(1 for data in self.fault_codes.values() if data.get('database') == 'TB')
        
        stats['hal_codes'] = hal_count
        stats['tb_codes'] = tb_count
        
        # Count by type
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
    print(f"HAL codes: {stats['hal_codes']}")
    print(f"TB codes: {stats['tb_codes']}")
    print(f"Types: {stats['types']}")
    print(f"Type breakdown: {stats['type_breakdown']}")
    
    # Test search
    test_code = "400027"
    result = parser.search_fault_code(test_code)
    if result:
        print(f"\nTest search for {test_code}:")
        print(f"Description: {result['description']}")
        print(f"Type: {result['type']}")
        print(f"Database: {result['database']} ({result['database_description']})")
    else:
        print(f"\nCode {test_code} not found")


if __name__ == "__main__":
    test_fault_parser()