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
            # Enhanced parameter patterns - more flexible for actual log files
            "water_parameters": re.compile(
                r"([a-zA-Z][a-zA-Z0-9_\s]*[a-zA-Z0-9])"  # Capture parameter name (letters, numbers, underscores, spaces)
                r"[:\s]*count\s*=\s*(\d+),?\s*"           # count=N
                r"max\s*=\s*([\d.-]+),?\s*"               # max=N.N
                r"min\s*=\s*([\d.-]+),?\s*"               # min=N.N  
                r"avg\s*=\s*([\d.-]+)",                   # avg=N.N
                re.IGNORECASE,
            ),
            # Serial number patterns
            "serial_number": re.compile(r"SN#?\s*(\d+)", re.IGNORECASE),
            "serial_alt": re.compile(r"Serial[:\s]+(\d+)", re.IGNORECASE),
            "machine_id": re.compile(r"Machine[:\s]+(\d+)", re.IGNORECASE),
        }

    def _init_parameter_mapping(self):
        """Initialize parameter mapping for trend tab parameters only"""
        self.parameter_mapping = {
            # Water/Flow parameters (for Water System tab)
            "magnetronFlow": {
                "patterns": [
                    "magnetron flow", "magnetronFlow", "CoolingmagnetronFlowLowStatistics",
                    "coolingmagnetronflowlowstatistics"
                ],
                "unit": "L/min",
                "description": "Mag Flow",
                "expected_range": (8, 18),
                "critical_range": (6, 20),
            },
            "targetAndCirculatorFlow": {
                "patterns": [
                    "target and circulator flow", "targetAndCirculatorFlow", 
                    "CoolingtargetFlowLowStatistics", "coolingtargetflowlowstatistics"
                ],
                "unit": "L/min",
                "description": "Flow Target",
                "expected_range": (6, 12),
                "critical_range": (4, 15),
            },
            "cityWaterFlow": {
                "patterns": [
                    "cooling city water flow statistics", "CoolingcityWaterFlowLowStatistics",
                    "cityWaterFlow", "city_water_flow"
                ],
                "unit": "L/min",
                "description": "Flow Chiller Water",
                "expected_range": (8, 18),
                "critical_range": (6, 20),
            },
            
            # Temperature parameters (for Temperature tab)
            "FanremoteTempStatistics": {
                "patterns": [
                    "FanremoteTempStatistics", "fanremotetempstatistics",
                    "Fan remote Temp Statistics", "remoteTempStatistics"
                ],
                "unit": "°C",
                "description": "Temp Room",
                "expected_range": (18, 25),
                "critical_range": (15, 30),
            },
            "magnetronTemp": {
                "patterns": [
                    "magnetronTemp", "magnetron temp", "magnetron temperature"
                ],
                "unit": "°C",
                "description": "Temp Magnetron",
                "expected_range": (30, 50),
                "critical_range": (20, 60),
            },
            
            # Humidity parameters (for Humidity tab)
            "FanhumidityStatistics": {
                "patterns": [
                    "FanhumidityStatistics", "fanhumiditystatistics",
                    "Fan humidity Statistics", "humidityStatistics"
                ],
                "unit": "%",
                "description": "Room Humidity",
                "expected_range": (40, 60),
                "critical_range": (30, 80),
            },
            
            # Fan speed parameters (for Fan Speed tab)
            "FanfanSpeed1Statistics": {
                "patterns": [
                    "FanfanSpeed1Statistics", "fanfanspeed1statistics",
                    "Fan fan Speed 1 Statistics", "fanSpeed1Statistics"
                ],
                "unit": "RPM",
                "description": "Speed FAN 1",
                "expected_range": (1000, 3000),
                "critical_range": (500, 4000),
            },
            "FanfanSpeed2Statistics": {
                "patterns": [
                    "FanfanSpeed2Statistics", "fanfanspeed2statistics",
                    "Fan fan Speed 2 Statistics", "fanSpeed2Statistics"
                ],
                "unit": "RPM",
                "description": "Speed FAN 2",
                "expected_range": (1000, 3000),
                "critical_range": (500, 4000),
            },
            "FanfanSpeed3Statistics": {
                "patterns": [
                    "FanfanSpeed3Statistics", "fanfanspeed3statistics",
                    "Fan fan Speed 3 Statistics", "fanSpeed3Statistics"
                ],
                "unit": "RPM",
                "description": "Speed FAN 3",
                "expected_range": (1000, 3000),
                "critical_range": (500, 4000),
            },
            "FanfanSpeed4Statistics": {
                "patterns": [
                    "FanfanSpeed4Statistics", "fanfanspeed4statistics",
                    "Fan fan Speed 4 Statistics", "fanSpeed4Statistics"
                ],
                "unit": "RPM",
                "description": "Speed FAN 4",
                "expected_range": (1000, 3000),
                "critical_range": (500, 4000),
            },
            
            # Voltage parameters (for Voltage tab)
            "MLC_ADC_CHAN_TEMP_BANKA_STAT_24V": {
                "patterns": [
                    "MLC_ADC_CHAN_TEMP_BANKA_STAT", "mlc_adc_chan_temp_banka_stat",
                    "MLC ADC CHAN TEMP BANKA STAT", "BANKA"
                ],
                "unit": "V",
                "description": "MLC Bank A 24V",
                "expected_range": (22, 26),
                "critical_range": (20, 28),
            },
            "MLC_ADC_CHAN_TEMP_BANKB_STAT_24V": {
                "patterns": [
                    "MLC_ADC_CHAN_TEMP_BANKB_STAT", "mlc_adc_chan_temp_bankb_stat",
                    "MLC ADC CHAN TEMP BANKB STAT", "BANKB"
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
                key = pattern.lower().replace(" ", "").replace(":", "").replace("_", "")
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
        """Enhanced line parsing with unified parameter mapping and filtering"""
        records = []

        # Extract datetime
        datetime_str = self._extract_datetime(line)
        if not datetime_str:
            return records

        # Extract serial number
        serial_number = self._extract_serial_number(line)

        # Extract parameters with statistics
        water_match = self.patterns["water_parameters"].search(line)
        if water_match:
            param_name = water_match.group(1).strip()

            # Debug output for actual log files
            if line_number <= 10:  # Only for first 10 lines to avoid spam
                print(f"Line {line_number}: Found parameter '{param_name}'")

            # Filter: Only process target parameters
            if not self._is_target_parameter(param_name):
                if line_number <= 10:
                    print(f"Line {line_number}: Parameter '{param_name}' filtered out")
                return records

            if line_number <= 10:
                print(f"Line {line_number}: Parameter '{param_name}' accepted for processing")

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
        # Remove spaces, colons, underscores, convert to lowercase for lookup
        lookup_key = param_name.lower().replace(" ", "").replace(":", "").replace("_", "")

        # Return unified name if found, otherwise return cleaned original
        return self.pattern_to_unified.get(lookup_key, param_name.strip())

    def _is_target_parameter(self, param_name: str) -> bool:
        """Check if parameter is one of the specific trend tab parameters only"""
        param_lower = param_name.lower().replace(" ", "").replace(":", "").replace("_", "")
        
        # Only allow parameters that match our exact trend tab parameter patterns
        target_patterns = []
        for param_config in self.parameter_mapping.values():
            for pattern in param_config["patterns"]:
                target_patterns.append(pattern.lower().replace(" ", "").replace(":", "").replace("_", ""))
        
        # Check if the parameter name contains any of our target patterns
        for pattern in target_patterns:
            pattern_clean = pattern.lower().replace(" ", "").replace(":", "").replace("_", "")
            if pattern_clean in param_lower or param_lower in pattern_clean:
                return True
        
        # Also check if it's in our pattern-to-unified mapping
        lookup_key = param_name.lower().replace(" ", "").replace(":", "").replace("_", "")
        if lookup_key in self.pattern_to_unified:
            return True
            
        return False

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

            # Create additional columns needed by database manager for compatibility
            if 'avg_value' in df.columns:
                # Create separate records for avg, min, max for database compatibility
                records = []
                for _, row in df.iterrows():
                    base_record = row.to_dict()
                    
                    # Average record
                    avg_record = base_record.copy()
                    avg_record['value'] = row['avg_value']
                    avg_record['statistic_type'] = 'avg'
                    records.append(avg_record)
                    
                    # Min record
                    min_record = base_record.copy()
                    min_record['value'] = row['min_value']
                    min_record['statistic_type'] = 'min'
                    records.append(min_record)
                    
                    # Max record
                    max_record = base_record.copy()
                    max_record['value'] = row['max_value']
                    max_record['statistic_type'] = 'max'
                    records.append(max_record)
                
                df = pd.DataFrame(records)

            # Reset index
            df = df.reset_index(drop=True)

            print(f"✓ Data cleaned: {len(df)} records ready for database")

        except Exception as e:
            print(f"Error cleaning data: {e}")

        return df

    # Fault Code Parsing Methods
    def load_fault_codes_from_uploaded_file(self, file_path: str) -> bool:
        """
        Load fault codes from uploaded file instead of fixed database.
        This addresses the requirement that fault code database should change
        with uploaded log files, not be permanent.
        """
        try:
            self.fault_codes = {}

            if not os.path.exists(file_path):
                return False

            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']

            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        for line_num, line in enumerate(file, 1):
                            line = line.strip()
                            if not line or line.startswith('#'):
                                continue

                            # Parse fault code line
                            fault_info = self._parse_fault_code_line(line)
                            if fault_info:
                                code = fault_info['code']
                                self.fault_codes[code] = {
                                    'description': fault_info['description'],
                                    'source': fault_info.get('source', 'uploaded'),
                                    'line_number': line_num
                                }

                    print(f"✓ Loaded {len(self.fault_codes)} fault codes from uploaded file")
                    return True

                except UnicodeDecodeError:
                    continue

            print(f"❌ Failed to load fault codes from {file_path}")
            return False

        except Exception as e:
            print(f"Error loading fault codes: {e}")
            return False

    def _parse_fault_code_line(self, line: str) -> Optional[Dict]:
        """Parse a single fault code line"""
        # Handle different fault code formats
        patterns = [
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
        """Search for fault code in loaded database"""
        code = str(code).strip()

        if code in self.fault_codes:
            return {
                'found': True,
                'code': code,
                'description': self.fault_codes[code]['description'],
                'source': self.fault_codes[code]['source'],
                'database_description': f"{self.fault_codes[code]['source'].title()} Database"
            }
        else:
            return {
                'found': False,
                'code': code,
                'description': 'Fault code not found in uploaded database',
                'source': 'none',
                'database_description': 'Not Available'
            }

    def get_fault_code_statistics(self) -> Dict:
        """Get statistics about loaded fault codes"""
        return {
            'total_codes': len(self.fault_codes),
            'sources': list(set(info['source'] for info in self.fault_codes.values())),
            'loaded_from': 'uploaded_file' if self.fault_codes else 'none'
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
        """Parse a single statistics log line from short data with filtering"""
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

            # Look for statistics pattern - extract parameter name after SN# portion
            # Find the parameter name between SN# and the colon
            param_match = re.search(r'SN#\s+\d+\s+(.+?)\s*:\s*count=', line)
            if not param_match:
                return None

            param_name_raw = param_match.group(1).strip()

            # Filter: Only process target parameters (water, voltage, humidity, temperature)
            if not self._is_target_parameter(param_name_raw):
                return None

            # Now extract the statistics
            stat_pattern = r'count=(\d+),?\s*max=([\d.-]+),?\s*min=([\d.-]+),?\s*avg=([\d.-]+)'
            stat_match = re.search(stat_pattern, line)

            if stat_match:
                param_name = self._normalize_parameter_name(param_name_raw)
                count = int(stat_match.group(1))
                max_val = float(stat_match.group(2))
                min_val = float(stat_match.group(3))
                avg_val = float(stat_match.group(4))

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

    def convert_short_data_to_dataframe(self, short_data_result: Dict) -> pd.DataFrame:
        """Convert parsed short data to DataFrame format compatible with analysis functions"""
        import pandas as pd

        if not short_data_result.get('success') or not short_data_result.get('parameters'):
            return pd.DataFrame()

        try:
            records = []
            parameters = short_data_result['parameters']

            for param in parameters:
                # Create records for each statistic type (avg, max, min)
                base_record = {
                    'datetime': param.get('datetime'),
                    'serial_number': param.get('serial_number', 'Unknown'),
                    'parameter_type': param.get('parameter_name', 'Unknown'),
                    'count': param.get('count', 0),
                    'line_number': param.get('line_number', 0)
                }

                # Add record for average value
                avg_record = base_record.copy()
                avg_record.update({
                    'statistic_type': 'avg',
                    'value': param.get('avg_value', 0),
                    'avg_value': param.get('avg_value', 0),
                    'max_value': param.get('max_value', 0),
                    'min_value': param.get('min_value', 0)
                })
                records.append(avg_record)

                # Add record for max value  
                max_record = base_record.copy()
                max_record.update({
                    'statistic_type': 'max',
                    'value': param.get('max_value', 0),
                    'avg_value': param.get('avg_value', 0),
                    'max_value': param.get('max_value', 0),
                    'min_value': param.get('min_value', 0)
                })
                records.append(max_record)

                # Add record for min value
                min_record = base_record.copy()
                min_record.update({
                    'statistic_type': 'min', 
                    'value': param.get('min_value', 0),
                    'avg_value': param.get('avg_value', 0),
                    'max_value': param.get('max_value', 0),
                    'min_value': param.get('min_value', 0)
                })
                records.append(min_record)

            # Create DataFrame
            df = pd.DataFrame(records)

            # Clean and validate the data
            df = self._clean_and_validate_data(df)

            return df

        except Exception as e:
            print(f"Error converting short data to DataFrame: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()

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

    def _get_parameter_data_by_description(self, parameter_description):
        """Get parameter data by its user-friendly description from the database"""
        try:
            if not hasattr(self, 'df') or self.df.empty:
                print("⚠️ No data available in database")
                return pd.DataFrame()

            print(f"🔍 DataFrame columns: {list(self.df.columns)}")
            print(f"🔍 DataFrame shape: {self.df.shape}")

            # Check which column name exists in the DataFrame
            param_column = None
            possible_columns = ['param', 'parameter_type', 'parameter_name']

            for col in possible_columns:
                if col in self.df.columns:
                    param_column = col
                    break

            if not param_column:
                print(f"⚠️ No parameter column found in DataFrame. Available columns: {list(self.df.columns)}")
                return pd.DataFrame()

            print(f"🔍 Using parameter column: '{param_column}'")

            # Enhanced mapping to match actual database format with partial string matching
            description_to_patterns = {
                "Mag Flow": ["magnetronFlow", "magnetron"],
                "Flow Target": ["targetAndCirculatorFlow", "target", "circulator"],
                "Flow Chiller Water": ["cityWaterFlow", "chiller", "city", "water"],
                "Temp Room": ["FanremoteTempStatistics", "remoteTemp", "roomTemp"],
                "Room Humidity": ["FanhumidityStatistics", "humidity"],
                "Temp Magnetron": ["magnetronTemp", "magnetron"],
                "Speed FAN 1": ["fanSpeed1", "FanSpeed1", "Speed1"],
                "Speed FAN 2": ["fanSpeed2", "FanSpeed2", "Speed2"],
                "Speed FAN 3": ["fanSpeed3", "FanSpeed3", "Speed3"],
                "Speed FAN 4": ["fanSpeed4", "FanSpeed4", "Speed4"],
                "MLC Bank A 24V": ["BANKA", "BankA", "24V"],
                "MLC Bank B 24V": ["BANKB", "BankB", "24V"],
            }

            # Get all available parameters
            all_params = self.df[param_column].unique()
            print(f"🔍 Available parameters: {all_params[:10]}")

            # Find matching parameter using enhanced pattern matching
            matching_params = []
            patterns = description_to_patterns.get(parameter_description, [parameter_description])

            print(f"🔍 Looking for patterns: {patterns}")

            # Enhanced search with flexible matching
            for pattern in patterns:
                for param in all_params:
                    param_lower = param.lower()
                    pattern_lower = pattern.lower()
                    
                    # Check if pattern is contained in the parameter name
                    if pattern_lower in param_lower and param not in matching_params:
                        matching_params.append(param)
                        print(f"✓ Pattern '{pattern}' matched parameter: '{param}'")

            # If no matches found, try even more flexible matching
            if not matching_params:
                print(f"🔍 No direct matches found, trying flexible matching...")
                # Try matching based on key words in the description
                key_words = {
                    "Mag Flow": ["magnetron", "flow"],
                    "Flow Target": ["target", "flow"],
                    "Flow Chiller Water": ["water", "flow"],
                    "Temp Room": ["temp", "remote", "fan"],
                    "Room Humidity": ["humidity", "fan"],
                    "Temp Magnetron": ["magnetron", "temp"],
                    "Speed FAN 1": ["speed", "fan", "1"],
                    "Speed FAN 2": ["speed", "fan", "2"],
                    "Speed FAN 3": ["speed", "fan", "3"],
                    "Speed FAN 4": ["speed", "fan", "4"],
                }
                
                if parameter_description in key_words:
                    words = key_words[parameter_description]
                    for param in all_params:
                        param_lower = param.lower()
                        if all(word.lower() in param_lower for word in words):
                            matching_params.append(param)
                            print(f"✓ Flexible match found: '{param}' for '{parameter_description}'")
                            break

            if matching_params:
                # Use the first matching parameter
                selected_param = matching_params[0]
                param_data = self.df[self.df[param_column] == selected_param].copy()
                print(f"✓ Using parameter: '{selected_param}'")
            else:
                print(f"⚠️ No data found for parameter '{parameter_description}'")
                print(f"⚠️ Available parameters: {all_params}")
                return pd.DataFrame()

            if param_data.empty:
                print(f"⚠️ Parameter data is empty for '{selected_param}'")
                return pd.DataFrame()

            # Sort by datetime and return in the format expected by plotting functions
            param_data = param_data.sort_values('datetime')

            # Check which value column exists
            value_column = None
            possible_value_columns = ['avg', 'average', 'avg_value', 'value']

            for col in possible_value_columns:
                if col in param_data.columns:
                    value_column = col
                    break

            if not value_column:
                print(f"⚠️ No value column found in DataFrame. Available columns: {list(param_data.columns)}")
                return pd.DataFrame()

            # Rename columns to match plotting expectations
            result_df = pd.DataFrame({
                'datetime': param_data['datetime'],
                'avg': param_data[value_column],
                'parameter_name': [parameter_description] * len(param_data)
            })

            print(f"✓ Retrieved {len(result_df)} data points for '{parameter_description}'")
            return result_df

        except Exception as e:
            print(f"❌ Error getting parameter data for '{parameter_description}': {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()