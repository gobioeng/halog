"""
Short Data Parser for HALog Application
Extracts additional parameters from shortdata.txt for enhanced diagnostics
Developer: HALog Enhancement Team
Company: gobioeng.com
"""

import re
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class ShortDataParser:
    """Parser for extracting enhanced parameters from shortdata.txt logs"""
    
    def __init__(self, file_path: Optional[str] = None):
        """Initialize the short data parser"""
        script_dir = Path(__file__).parent
        
        if file_path is None:
            file_path = script_dir / "data" / "shortdata.txt"
        
        self.file_path = Path(file_path)
        self.extracted_data = {}
        self.parameter_groups = {
            'temperature': [],
            'voltage': [],
            'humidity': [],
            'fan_speed': [],
            'flow': [],
            'pressure': []
        }
    
    def parse_log_file(self) -> Dict:
        """Parse the shortdata.txt file and extract parameters"""
        if not self.file_path.exists():
            print(f"Warning: Short data file not found at {self.file_path}")
            return {}
        
        print(f"📊 Parsing short data file: {self.file_path}")
        
        try:
            # Read file with multiple encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            content = None
            
            for encoding in encodings:
                try:
                    with open(self.file_path, 'r', encoding=encoding) as f:
                        content = f.readlines()
                    print(f"✓ Successfully read file with {encoding} encoding")
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                print("❌ Failed to read file with any encoding")
                return {}
            
            extracted_params = []
            debug_count = 0
            
            for line_num, line in enumerate(content, 1):
                line = line.strip()
                if not line:
                    continue
                
                if 'logStatistics' in line:
                    debug_count += 1
                    if debug_count <= 3:  # Debug first few lines
                        print(f"🔍 Debug line {line_num}: {line}")
                    
                    # Parse log line
                    param_data = self._parse_statistics_line(line, line_num)
                    if param_data:
                        extracted_params.append(param_data)
                        if debug_count <= 3:
                            print(f"✓ Parsed: {param_data}")
            
            print(f"🔍 Found {debug_count} logStatistics lines, extracted {len(extracted_params)} parameters")
            
            # Group parameters by type
            self._group_parameters(extracted_params)
            
            print(f"✓ Extracted {len(extracted_params)} parameter entries")
            self._print_summary()
            
            return {
                'parameters': extracted_params,
                'groups': self.parameter_groups
            }
            
        except Exception as e:
            print(f"❌ Error parsing short data file: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def _parse_statistics_line(self, line: str, line_num: int) -> Optional[Dict]:
        """Parse a single statistics log line"""
        try:
            # Pattern to match log format:
            # Date Time Local0 Info Time SN# XXXX Component Type Class::method message
            
            # Extract basic info - split by tabs
            parts = line.split('\t')
            if len(parts) < 8:
                return None
            
            date_str = parts[0]
            time_str = parts[1]
            log_time = parts[4]
            component_info = parts[6] if len(parts) > 6 else ""
            class_type = parts[7] if len(parts) > 7 else ""
            message = parts[8] if len(parts) > 8 else ""
            
            # Extract serial number
            sn_match = re.search(r'SN# (\d+)', line)
            serial_number = sn_match.group(1) if sn_match else "Unknown"
            
            # Extract parameter name and statistics from the message
            if 'logStatistics' in message:
                # Pattern: Class::logStatistics ParameterName: count=X, max=Y, min=Z, avg=W
                stat_match = re.search(r'logStatistics\s+([^:]+):\s*count=(\d+),\s*max=([\d.-]+),\s*min=([\d.-]+),\s*avg=([\d.-]+)', message)
                
                if stat_match:
                    param_name = stat_match.group(1).strip()
                    
                    # Clean up parameter name - fix common naming issues
                    param_name = self._normalize_parameter_name(param_name)
                    
                    count = int(stat_match.group(2))
                    max_val = float(stat_match.group(3))
                    min_val = float(stat_match.group(4))
                    avg_val = float(stat_match.group(5))
                    
                    # Create datetime
                    try:
                        datetime_str = f"{date_str} {time_str}"
                        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
                    except:
                        dt = None
                    
                    return {
                        'datetime': dt,
                        'serial_number': serial_number,
                        'component': component_info,
                        'parameter_name': param_name,
                        'count': count,
                        'max_value': max_val,
                        'min_value': min_val,
                        'avg_value': avg_val,
                        'line_number': line_num
                    }
        
        except Exception as e:
            print(f"Warning: Error parsing line {line_num}: {e}")
        
        return None
    
    def _normalize_parameter_name(self, param_name: str) -> str:
        """Normalize parameter names to fix common naming issues"""
        # Fix double "Fan" prefix in fan speed parameters
        if param_name.startswith('FanfanSpeed'):
            param_name = param_name.replace('FanfanSpeed', 'FanSpeed')
        
        # Add other normalizations as needed
        # For example, fix case consistency or remove redundant prefixes
        
        return param_name
    
    def _group_parameters(self, parameters: List[Dict]):
        """Group parameters by type for organized visualization - Enhanced for requirement specifications"""
        for param in parameters:
            param_name = param['parameter_name'].lower()
            original_name = param['parameter_name']
            
            # Fan speed parameters (check first to catch fan-related temps)
            if any(term in param_name for term in ['fanspeed', 'fan speed']):
                self.parameter_groups['fan_speed'].append(param)
            
            # Voltage parameters (enhanced patterns)
            elif any(term in param_name for term in [
                'volt', '_v_', 'vref', '24v', '48v', '5v', '3v', '15v', '11v', '10v',
                'mlc_adc_chan_', 'col_adc_chan_', 'motorpwr', 'motor_pwr'
            ]):
                self.parameter_groups['voltage'].append(param)
            
            # Temperature parameters (enhanced patterns)
            elif any(term in param_name for term in [
                'temp', 'temperature', 'thermal', 'fanremotetemp', 'pdu_boardtemp',
                'col_board_temp', 'magnetrontemp', 'watertanktemp'
            ]):
                self.parameter_groups['temperature'].append(param)
            
            # Humidity parameters (include room temp per requirements)
            elif any(term in param_name for term in ['humidity', 'fanremotetemp']):
                self.parameter_groups['humidity'].append(param)
            
            # Flow parameters (enhanced patterns for water system)
            elif any(term in param_name for term in [
                'flow', 'magnetronflow', 'targetflow', 'citywater', 'chiller'
            ]):
                self.parameter_groups['flow'].append(param)
            
            # Pressure parameters
            elif any(term in param_name for term in ['pressure', 'pumppressure']):
                self.parameter_groups['pressure'].append(param)
    
    def _print_summary(self):
        """Print summary of extracted parameters"""
        print("\n📋 Parameter Summary:")
        for group_name, params in self.parameter_groups.items():
            if params:
                unique_params = set(p['parameter_name'] for p in params)
                print(f"  {group_name.title()}: {len(unique_params)} unique parameters, {len(params)} entries")
                
                # Show some examples
                if len(unique_params) > 0:
                    examples = list(unique_params)[:3]
                    print(f"    Examples: {', '.join(examples)}")
    
    def get_parameters_by_group(self, group_name: str) -> List[Dict]:
        """Get parameters by group name"""
        return self.parameter_groups.get(group_name, [])
    
    def get_unique_parameter_names(self, group_name: str) -> List[str]:
        """Get unique parameter names for a group"""
        params = self.get_parameters_by_group(group_name)
        return list(set(p['parameter_name'] for p in params))
    
    def get_data_for_visualization(self, group_name: str, parameter_name: str = None) -> pd.DataFrame:
        """Get data formatted for visualization"""
        params = self.get_parameters_by_group(group_name)
        
        if parameter_name:
            params = [p for p in params if p['parameter_name'] == parameter_name]
        
        if not params:
            return pd.DataFrame()
        
        # Convert to DataFrame
        df_data = []
        for param in params:
            df_data.append({
                'datetime': param['datetime'],
                'serial_number': param['serial_number'],
                'parameter': param['parameter_name'],
                'avg_value': param['avg_value'],
                'min_value': param['min_value'],
                'max_value': param['max_value'],
                'count': param['count']
            })
        
        df = pd.DataFrame(df_data)
        return df.sort_values('datetime') if 'datetime' in df.columns else df


def test_shortdata_parser():
    """Test function for the short data parser"""
    parser = ShortDataParser()
    result = parser.parse_log_file()
    
    if result:
        print("\n🧪 Testing parameter extraction:")
        
        # Test each group
        for group_name in ['temperature', 'voltage', 'humidity', 'fan_speed', 'flow']:
            params = parser.get_unique_parameter_names(group_name)
            if params:
                print(f"\n{group_name.title()} Parameters:")
                for param in params[:5]:  # Show first 5
                    print(f"  - {param}")
                
                # Test data extraction for first parameter
                if params:
                    df = parser.get_data_for_visualization(group_name, params[0])
                    if not df.empty:
                        print(f"  Data points for '{params[0]}': {len(df)}")


if __name__ == "__main__":
    test_shortdata_parser()