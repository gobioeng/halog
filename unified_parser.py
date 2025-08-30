"""
Unified Parser for HALog Application
Consolidates LINAC log parsing, fault code parsing, and short data parsing
into a single comprehensive parser module.

This addresses the requirement to use only one file for data parsing
instead of multiple separate parser files.

Developer: HALog Enhancement Team  
Company: gobioeng.com
"""

import pandas as pd
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import os
from pathlib import Path


class UnifiedParser:
    """
    Unified parser for all HALog data types:
    - LINAC log files (water system parameters, temperatures, voltages, etc.)
    - Fault code databases (dynamic loading from uploaded files)
    - Short data files (additional diagnostic parameters)
    """

    def __init__(self):
        self._compile_patterns()
        self._init_parameter_mapping()
        self.parsing_stats = {
            "lines_processed": 0,
            "records_extracted": 0,
            "errors_encountered": 0,
            "processing_time": 0,
        }
        self.fault_codes: Dict[str, Dict[str, str]] = {}
        # Load static fault codes during initialization
        self.load_static_fault_codes()
        
    def _compile_patterns(self):
        """Compile regex patterns for enhanced log parsing"""
        self.patterns = {
            # Enhanced datetime patterns
            "datetime": re.compile(
                r"(\d{4}-\d{2}-\d{2})[ \t]+(\d{2}:\d{2}:\d{2})", re.IGNORECASE
            ),
            "datetime_alt": re.compile(
                r"(\d{1,2}/\d{1,2}/\d{4})[ \t]+(\d{1,2}:\d{2}:\d{2})"
            ),
            # Enhanced water system parameter patterns
            "water_parameters": re.compile(
                r"("
                r"cooling\s*pump\s*high\s*statistics|CoolingpumpHighStatistics|pumpPressure|PumpPressure|pump_pressure|"
                r"magnetron\s*flow|magnetronFlow|CoolingmagnetronFlowLowStatistics|coolingmagnetronflowlowstatistics|"
                r"target\s*(?:and\s*)?circulator\s*flow|targetAndCirculatorFlow|coolingtargetflowlowstatistics|"
                r"cooling\s*city\s*water\s*flow\s*statistics|CoolingcityWaterFlowLowStatistics|cityWaterFlow|city_water_flow"
                r")"
                r"[:\s]*count=(\d+),?\s*"
                r"max=([\d.]+),?\s*"
                r"min=([\d.]+),?\s*"
                r"avg=([\d.]+)",
                re.IGNORECASE,
            ),
            # Serial number patterns
            "serial_number": re.compile(r"SN#?\s*(\d+)", re.IGNORECASE),
            "serial_alt": re.compile(r"Serial[:\s]+(\d+)", re.IGNORECASE),
            "machine_id": re.compile(r"Machine[:\s]+(\d+)", re.IGNORECASE),
        }

    def _init_parameter_mapping(self):
        """Initialize unified parameter mapping with all real log variants"""
        self.parameter_mapping = {
            "pumpPressure": {
                "patterns": [
                    "cooling pump high statistics",
                    "CoolingpumpHighStatistics",
                    "pump_pressure",
                ],
                "unit": "PSI",
                "description": "Cooling Pump Pressure",
                "expected_range": (170, 230),
                "critical_range": (160, 240),
            },
            "magnetronFlow": {
                "patterns": [
                    "magnetron flow",
                    "magnetronFlow",
                    "CoolingmagnetronFlowLowStatistics",
                ],
                "unit": "L/min",
                "description": "Mag Flow",
                "expected_range": (8, 18),
                "critical_range": (6, 20),
            },
            "targetFlow": {
                "patterns": [
                    "target and circulator flow",
                    "targetAndCirculatorFlow",
                    "CoolingtargetFlowLowStatistics",
                ],
                "unit": "L/min",
                "description": "Flow Target",
                "expected_range": (6, 12),
                "critical_range": (4, 15),
            },
            "cityWaterFlow": {
                "patterns": [
                    "cooling city water flow statistics",
                    "CoolingcityWaterFlowLowStatistics",
                    "cityWaterFlow",
                    "city_water_flow",
                ],
                "unit": "L/min",
                "description": "Flow Chiller Water",
                "expected_range": (8, 18),
                "critical_range": (6, 20),
            },
            # Temperature parameters
            "CoolingtargetTempStatistics": {
                "patterns": [
                    "CoolingtargetTempStatistics",
                    "Cooling target Temp Statistics",
                    "targetTempStatistics",
                ],
                "unit": "°C",
                "description": "Flow Target",
                "expected_range": (40, 80),
                "critical_range": (30, 90),
            },
            "FanremoteTempStatistics": {
                "patterns": [
                    "FanremoteTempStatistics",
                    "Fan remote Temp Statistics",
                    "remoteTempStatistics",
                ],
                "unit": "°C",
                "description": "Temp Room",
                "expected_range": (18, 25),
                "critical_range": (15, 30),
            },
            "FanhumidityStatistics": {
                "patterns": [
                    "FanhumidityStatistics",
                    "Fan humidity Statistics",
                    "humidityStatistics",
                ],
                "unit": "%",
                "description": "Room Humidity",
                "expected_range": (40, 60),
                "critical_range": (30, 80),
            },
            # Fan speed parameters
            "FanfanSpeed1Statistics": {
                "patterns": [
                    "FanfanSpeed1Statistics",
                    "Fan fan Speed 1 Statistics",
                    "fanSpeed1Statistics",
                ],
                "unit": "RPM",
                "description": "Speed FAN 1",
                "expected_range": (1000, 3000),
                "critical_range": (500, 4000),
            },
            "FanfanSpeed2Statistics": {
                "patterns": [
                    "FanfanSpeed2Statistics", 
                    "Fan fan Speed 2 Statistics",
                    "fanSpeed2Statistics",
                ],
                "unit": "RPM",
                "description": "Speed FAN 2",
                "expected_range": (1000, 3000),
                "critical_range": (500, 4000),
            },
            "FanfanSpeed3Statistics": {
                "patterns": [
                    "FanfanSpeed3Statistics",
                    "Fan fan Speed 3 Statistics",
                    "fanSpeed3Statistics",
                ],
                "unit": "RPM",
                "description": "Speed FAN 3",
                "expected_range": (1000, 3000),
                "critical_range": (500, 4000),
            },
            "FanfanSpeed4Statistics": {
                "patterns": [
                    "FanfanSpeed4Statistics",
                    "Fan fan Speed 4 Statistics", 
                    "fanSpeed4Statistics",
                ],
                "unit": "RPM",
                "description": "Speed FAN 4",
                "expected_range": (1000, 3000),
                "critical_range": (500, 4000),
            },
            # Voltage parameters
            "MLC_ADC_CHAN_TEMP_BANKA_STAT_24V": {
                "patterns": [
                    "MLC_ADC_CHAN_TEMP_BANKA_STAT",
                    "MLC ADC CHAN TEMP BANKA STAT",
                ],
                "unit": "V",
                "description": "MLC Bank A 24V", 
                "expected_range": (22, 26),
                "critical_range": (20, 28),
            },
            "MLC_ADC_CHAN_TEMP_BANKB_STAT_24V": {
                "patterns": [
                    "MLC_ADC_CHAN_TEMP_BANKB_STAT",
                    "MLC ADC CHAN TEMP BANKB STAT",
                ],
                "unit": "V",
                "description": "MLC Bank B 24V",
                "expected_range": (22, 26),
                "critical_range": (20, 28),
            },
        }

        # Create pattern to unified name mapping
        self.pattern_to_unified = {}
        for unified_name, config in self.parameter_mapping.items():
            for pattern in config["patterns"]:
                key = pattern.lower().replace(" ", "").replace(":", "")
                self.pattern_to_unified[key] = unified_name

    def parse_linac_file(
        self,
        file_path: str,
        chunk_size: int = 1000,
        progress_callback=None,
        cancel_callback=None,
    ) -> pd.DataFrame:
        """Parse LINAC log file with chunked processing for large files"""
        records = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
            total_lines = len(lines)
            self.parsing_stats["lines_processed"] = 0
            
            for i in range(0, total_lines, chunk_size):
                if cancel_callback and cancel_callback():
                    break
                    
                chunk_lines = [(i + j, lines[i + j].strip()) 
                              for j in range(min(chunk_size, total_lines - i))]
                
                chunk_records = self._process_chunk(chunk_lines)
                records.extend(chunk_records)
                
                self.parsing_stats["lines_processed"] += len(chunk_lines)
                
                if progress_callback:
                    progress = (i + len(chunk_lines)) / total_lines * 100
                    progress_callback(progress)
                    
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            self.parsing_stats["errors_encountered"] += 1
            
        df = pd.DataFrame(records)
        return self._clean_and_validate_data(df)

    def _process_chunk(self, chunk_lines: List[Tuple[int, str]]) -> List[Dict]:
        """Process a chunk of lines"""
        records = []
        
        for line_number, line in chunk_lines:
            try:
                parsed_records = self._parse_line_enhanced(line, line_number)
                records.extend(parsed_records)
            except Exception as e:
                self.parsing_stats["errors_encountered"] += 1
                
        return records

    def _parse_line_enhanced(self, line: str, line_number: int) -> List[Dict]:
        """Enhanced line parsing with unified parameter mapping"""
        records = []
        
        # Extract datetime
        datetime_str = self._extract_datetime(line)
        if not datetime_str:
            return records
            
        # Extract serial number
        serial_number = self._extract_serial_number(line)
        
        # Extract water system parameters
        water_match = self.patterns["water_parameters"].search(line)
        if water_match:
            param_name = water_match.group(1).strip()
            count = int(water_match.group(2))
            max_val = float(water_match.group(3))
            min_val = float(water_match.group(4))
            avg_val = float(water_match.group(5))
            
            # Normalize parameter name
            normalized_param = self._normalize_parameter_name(param_name)
            
            record = {
                'datetime': datetime_str,
                'serial_number': serial_number,
                'parameter_type': normalized_param,
                'statistic_type': 'combined',
                'count': count,
                'max_value': max_val,
                'min_value': min_val,
                'avg_value': avg_val,
                'line_number': line_number,
                'quality': self._assess_data_quality(normalized_param, avg_val, count)
            }
            records.append(record)
            
        return records

    def _extract_datetime(self, line: str) -> Optional[str]:
        """Extract datetime with multiple pattern support"""
        # Try primary datetime pattern
        match = self.patterns["datetime"].search(line)
        if match:
            date_part = match.group(1)
            time_part = match.group(2)
            return f"{date_part} {time_part}"

        # Try alternative datetime pattern
        match = self.patterns["datetime_alt"].search(line)
        if match:
            date_part = match.group(1)
            time_part = match.group(2)
            
            # Convert MM/DD/YYYY to YYYY-MM-DD
            try:
                date_obj = datetime.strptime(date_part, "%m/%d/%Y")
                formatted_date = date_obj.strftime("%Y-%m-%d")
                return f"{formatted_date} {time_part}"
            except ValueError:
                pass

        return None

    def _extract_serial_number(self, line: str) -> str:
        """Extract serial number from line"""
        # Try primary serial number pattern
        match = self.patterns["serial_number"].search(line)
        if match:
            return match.group(1)
            
        # Try alternative patterns
        match = self.patterns["serial_alt"].search(line)
        if match:
            return match.group(1)
            
        match = self.patterns["machine_id"].search(line)
        if match:
            return match.group(1)
            
        return "Unknown"

    def _normalize_parameter_name(self, param_name: str) -> str:
        """Normalize parameter names to fix common naming issues"""
        # Remove spaces, colons, convert to lowercase for lookup
        lookup_key = param_name.lower().replace(" ", "").replace(":", "")
        
        # Return unified name if found, otherwise return cleaned original
        return self.pattern_to_unified.get(lookup_key, param_name.strip())

    def _assess_data_quality(self, param_name: str, value: float, count: int) -> str:
        """Assess data quality for each reading"""
        if param_name not in self.parameter_mapping:
            return "unknown"

        config = self.parameter_mapping[param_name]
        expected_min, expected_max = config["expected_range"]

        # Quality assessment
        if expected_min <= value <= expected_max:
            if count > 100:
                return "excellent"
            elif count > 50:
                return "good"
            else:
                return "fair"
        else:
            return "poor"

    def _clean_and_validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate the parsed data"""
        if df.empty:
            return df

        try:
            # Convert datetime
            df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

            # Remove rows with invalid datetime
            df = df.dropna(subset=["datetime"])

            # Sort by datetime
            df = df.sort_values("datetime")

            # Remove duplicates
            df = df.drop_duplicates(
                subset=["datetime", "serial_number", "parameter_type", "statistic_type"]
            )

            # Reset index
            df = df.reset_index(drop=True)

        except Exception as e:
            print(f"Error cleaning data: {e}")

        return df

    # Fault Code Database Methods - STATIC DATABASE
    def load_static_fault_codes(self) -> bool:
        """
        Load fault codes from static database files in the core application.
        Fault code database is fixed and does not change with log uploads.
        """
        try:
            script_dir = Path(__file__).parent
            hal_file_path = script_dir / "data" / "HALfault.txt"
            tb_file_path = script_dir / "data" / "TBFault.txt"
            
            self.fault_codes = {}
            
            # Load HAL fault codes
            success_hal = self._load_static_fault_file(hal_file_path, "HAL")
            
            # Load TB fault codes
            success_tb = self._load_static_fault_file(tb_file_path, "TB")
            
            total_loaded = len(self.fault_codes)
            if total_loaded > 0:
                print(f"✓ Static fault code database loaded: {total_loaded} codes from core files")
                return True
            else:
                print("❌ No fault codes loaded from static database")
                return False
                
        except Exception as e:
            print(f"Error loading static fault codes: {e}")
            return False

    def _load_static_fault_file(self, file_path: Path, database_source: str) -> bool:
        """Load fault codes from a static core fault file"""
        try:
            if not file_path.exists():
                print(f"Warning: Static fault file not found at {file_path}")
                return False
            
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            lines = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        lines = file.readlines()
                    break
                except UnicodeDecodeError:
                    continue
            
            if lines is None:
                print(f"Error: Could not read {database_source} fault file")
                return False
            
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
            
            print(f"✓ Loaded {codes_loaded} codes from static {database_source} database")
            return True
            
        except Exception as e:
            print(f"Error loading static {database_source} fault codes: {e}")
            return False

    def _parse_fault_code_line(self, line: str) -> Optional[Dict]:
        """Parse a single fault code line from static database"""
        # Handle different fault code formats for static files
        patterns = [
            r'^(\d+)\s*\t+(.+)$',  # "12345\tDescription"
            r'^(\d+)\s*[:\-\s]+(.+)$',  # "12345: Description"
            r'^(\d+)\s+(.+)$',          # "12345 Description"
            r'^Code\s*(\d+)\s*[:\-\s]*(.+)$',  # "Code 12345: Description"
        ]
        
        for pattern in patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                return {
                    'code': match.group(1).strip(),
                    'description': match.group(2).strip()
                }
        
        return None

    def search_fault_code(self, code: str) -> Dict:
        """Search for fault code in static database"""
        code = str(code).strip()
        
        if code in self.fault_codes:
            fault_info = self.fault_codes[code]
            return {
                'found': True,
                'code': code,
                'description': fault_info['description'],
                'type': fault_info.get('type', 'Unknown'),
                'database': fault_info['database'],
                'database_description': f"{fault_info['database']} Database"
            }
        else:
            return {
                'found': False,
                'code': code,
                'description': 'Fault code not found in static database',
                'type': 'Unknown',
                'database': 'none',
                'database_description': 'Not Available'
            }

    def get_fault_code_statistics(self) -> Dict:
        """Get statistics about static fault code database"""
        databases = list(set(info['database'] for info in self.fault_codes.values()))
        return {
            'total_codes': len(self.fault_codes),
            'databases': databases,
            'loaded_from': 'static_core_files'
        }

    # Short Data Parsing Methods
    def parse_short_data_file(self, file_path: str) -> Dict:
        """Parse shortdata.txt file for additional parameters"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
            parameters = []
            for line_num, line in enumerate(lines, 1):
                parsed = self._parse_statistics_line(line, line_num)
                if parsed:
                    parameters.append(parsed)
                    
            grouped_params = self._group_parameters(parameters)
            
            return {
                'success': True,
                'parameters': parameters,
                'grouped_parameters': grouped_params,
                'total_parameters': len(parameters)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'parameters': [],
                'grouped_parameters': {},
                'total_parameters': 0
            }

    def _parse_statistics_line(self, line: str, line_num: int) -> Optional[Dict]:
        """Parse a single statistics log line from short data"""
        try:
            # Extract basic info - split by tabs
            parts = line.split('\t')
            if len(parts) < 8:
                return None
            
            date_str = parts[0]
            time_str = parts[1]
            
            # Extract serial number
            sn_match = re.search(r'SN# (\d+)', line)
            serial_number = sn_match.group(1) if sn_match else "Unknown"
            
            # Look for statistics pattern
            stat_pattern = r'(\w+)\s*:\s*count=(\d+),?\s*max=([\d.-]+),?\s*min=([\d.-]+),?\s*avg=([\d.-]+)'
            stat_match = re.search(stat_pattern, line)
            
            if stat_match:
                param_name = self._normalize_parameter_name(stat_match.group(1))
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

    def _group_parameters(self, parameters: List[Dict]) -> Dict:
        """Group parameters by type for organized visualization"""
        groups = {
            'water_system': [],
            'temperatures': [],
            'voltages': [],
            'humidity': [],
            'fan_speeds': [],
            'other': []
        }
        
        for param in parameters:
            param_name = param['parameter_name'].lower()
            
            if any(keyword in param_name for keyword in ['flow', 'pump', 'water']):
                groups['water_system'].append(param)
            elif any(keyword in param_name for keyword in ['temp', 'temperature']):
                groups['temperatures'].append(param)
            elif any(keyword in param_name for keyword in ['voltage', 'volt', 'v']):
                groups['voltages'].append(param)
            elif any(keyword in param_name for keyword in ['humidity', 'humid']):
                groups['humidity'].append(param)
            elif any(keyword in param_name for keyword in ['fan', 'speed']):
                groups['fan_speeds'].append(param)
            else:
                groups['other'].append(param)
                
        return groups

    # Utility Methods
    def get_supported_parameters(self) -> Dict:
        """Get information about supported parameters"""
        return {
            param: {
                "unit": config["unit"],
                "description": config["description"],
                "expected_range": config["expected_range"],
            }
            for param, config in self.parameter_mapping.items()
        }

    def get_parsing_stats(self) -> Dict:
        """Get parsing statistics"""
        return self.parsing_stats.copy()

    def get_simplified_parameter_names(self) -> List[Dict]:
        """
        Get simplified parameter names for dashboard display.
        This addresses the requirement to show simplified names instead of 
        parameter counts.
        """
        simplified = []
        
        for param_key, config in self.parameter_mapping.items():
            simplified.append({
                'key': param_key,
                'name': config['description'],
                'unit': config['unit'],
                'category': self._categorize_parameter(param_key)
            })
            
        return simplified

    def _categorize_parameter(self, param_key: str) -> str:
        """Categorize parameter for grouping"""
        key_lower = param_key.lower()
        
        if 'flow' in key_lower or 'pump' in key_lower:
            return 'Water System'
        elif 'temp' in key_lower:
            return 'Temperature'
        elif 'speed' in key_lower or 'fan' in key_lower:
            return 'Fan Speed'
        elif 'humidity' in key_lower:
            return 'Humidity'
        elif 'mlc' in key_lower or 'volt' in key_lower or 'v' in param_key:
            return 'Voltage'
        else:
            return 'Other'