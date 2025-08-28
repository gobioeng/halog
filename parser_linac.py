import pandas as pd
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import os


class LinacParser:
    """Enhanced LINAC log parser with unified parameter mapping and improved performance"""

    def __init__(self):
        self._compile_patterns()
        self._init_parameter_mapping()
        self.parsing_stats = {
            "lines_processed": 0,
            "records_extracted": 0,
            "errors_encountered": 0,
            "processing_time": 0,
        }

    def _compile_patterns(self):
        """Compile regex patterns for enhanced log parsing"""
        # Expanded regex to match spaced, unspaced, and camelCase variants
        self.patterns = {
            # Enhanced datetime patterns
            "datetime": re.compile(
                r"(\d{4}-\d{2}-\d{2})[ \t]+(\d{2}:\d{2}:\d{2})", re.IGNORECASE
            ),
            "datetime_alt": re.compile(
                r"(\d{1,2}/\d{1,2}/\d{4})[ \t]+(\d{1,2}:\d{2}:\d{2})"
            ),
            # Enhanced water system parameter patterns with unified mapping
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
            # Serial number patterns are unchanged
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
                    "coolingpumphighstatistics",
                    "CoolingpumpHighStatistics",
                    "pumpPressure",
                    "PumpPressure",
                    "pump_pressure",
                ],
                "unit": "PSI",
                "description": "Cooling Pump Pressure Statistics",
                "expected_range": (170, 230),
                "critical_range": (160, 240),
            },
            "magnetronFlow": {
                "patterns": [
                    "magnetron flow",
                    "magnetronFlow",
                    "cooling magnetron flow low statistics",
                    "coolingmagnetronflowlowstatistics",
                    "CoolingmagnetronFlowLowStatistics",
                ],
                "unit": "L/min",
                "description": "Mag Flow",
                "expected_range": (3, 10),
                "critical_range": (2, 12),
            },
            "targetAndCirculatorFlow": {
                "patterns": [
                    "target and circulator flow",
                    "targetAndCirculatorFlow",
                    "target circulator flow",
                    "cooling target flow low statistics",
                    "coolingtargetflowlowstatistics",
                ],
                "unit": "L/min",
                "description": "Flow Target",
                "expected_range": (2, 5),
                "critical_range": (1, 6),
            },
            "cityWaterFlow": {
                "patterns": [
                    "cooling city water flow statistics",
                    "CoolingcityWaterFlowLowStatistics",
                    "cooling city water flow low statistics",
                    "coolingcitywaterflowlowstatistics",
                    "cooling citywaterflowstatistics",
                    "cityWaterFlow",
                    "city_water_flow",
                ],
                "unit": "L/min",
                "description": "Flow Chiller Water",
                "expected_range": (8, 18),
                "critical_range": (6, 20),
            },
            # Enhanced parameter mappings as per requirements
            "MLC_ADC_CHAN_TEMP_BANKB_STAT_24V": {
                "patterns": [
                    "MLC_ADC_CHAN_TEMP_BANKB_STAT",
                    "mlc_adc_chan_temp_bankb_stat",
                    "MLC ADC CHAN TEMP BANKB STAT",
                ],
                "unit": "V",
                "description": "MLC Bank B 24V",
                "expected_range": (22, 26),
                "critical_range": (20, 28),
            },
            "MLC_ADC_CHAN_TEMP_BANKA_STAT_24V": {
                "patterns": [
                    "MLC_ADC_CHAN_TEMP_BANKA_STAT",
                    "mlc_adc_chan_temp_banka_stat", 
                    "MLC ADC CHAN TEMP BANKA STAT",
                ],
                "unit": "V",
                "description": "MLC Bank A 24V",
                "expected_range": (22, 26),
                "critical_range": (20, 28),
            },
            "FanfanSpeed1Statistics": {
                "patterns": [
                    "FanfanSpeed1Statistics",
                    "fanfanspeed1statistics",
                    "Fan fan Speed 1 Statistics",
                    "fanSpeed1",
                ],
                "unit": "RPM",
                "description": "Speed FAN 1",
                "expected_range": (1000, 3000),
                "critical_range": (500, 4000),
            },
            "FanfanSpeed2Statistics": {
                "patterns": [
                    "FanfanSpeed2Statistics",
                    "fanfanspeed2statistics",
                    "Fan fan Speed 2 Statistics",
                    "fanSpeed2",
                ],
                "unit": "RPM",
                "description": "Speed FAN 2",
                "expected_range": (1000, 3000),
                "critical_range": (500, 4000),
            },
            "FanfanSpeed3Statistics": {
                "patterns": [
                    "FanfanSpeed3Statistics",
                    "fanfanspeed3statistics",
                    "Fan fan Speed 3 Statistics",
                    "fanSpeed3",
                ],
                "unit": "RPM",
                "description": "Speed FAN 3",
                "expected_range": (1000, 3000),
                "critical_range": (500, 4000),
            },
            "FanfanSpeed4Statistics": {
                "patterns": [
                    "FanfanSpeed4Statistics",
                    "fanfanspeed4statistics",
                    "Fan fan Speed 4 Statistics",
                    "fanSpeed4",
                ],
                "unit": "RPM",
                "description": "Speed FAN 4",
                "expected_range": (1000, 3000),
                "critical_range": (500, 4000),
            },
            "CoolingtargetTempStatistics": {
                "patterns": [
                    "CoolingtargetTempStatistics",
                    "coolingtargettempstatistics",
                    "Cooling target Temp Statistics",
                    "targetTempStatistics",
                ],
                "unit": "L/min",
                "description": "Flow Target",
                "expected_range": (2, 5),
                "critical_range": (1, 6),
            },
            "FanremoteTempStatistics": {
                "patterns": [
                    "FanremoteTempStatistics",
                    "fanremotetempstatistics",
                    "Fan remote Temp Statistics",
                    "remoteTempStatistics",
                ],
                "unit": "°C",
                "description": "Temp Room",
                "expected_range": (18, 25),
                "critical_range": (15, 30),
            },
            "pdu_boardTemp_STAT": {
                "patterns": [
                    "pdu_boardTemp_STAT",
                    "pdu_boardtemp_stat",
                    "PDU board Temp STAT",
                    "pduBoardTemp",
                ],
                "unit": "°C",
                "description": "Temp PDU",
                "expected_range": (20, 40),
                "critical_range": (15, 50),
            },
            "COL_ADC_CHAN_M48V_MON_STAT": {
                "patterns": [
                    "COL_ADC_CHAN_M48V_MON_STAT",
                    "col_adc_chan_m48v_mon_stat",
                    "COL ADC CHAN M48V MON STAT",
                ],
                "unit": "V",
                "description": "COL 48V",
                "expected_range": (-50, -46),
                "critical_range": (-52, -44),
            },
            "MLC_ADC_CHAN_M48V_BANKA_MON_STAT": {
                "patterns": [
                    "MLC_ADC_CHAN_M48V_BANKA_MON_STAT",
                    "mlc_adc_chan_m48v_banka_mon_stat",
                    "MLC ADC CHAN M48V BANKA MON STAT",
                ],
                "unit": "V",
                "description": "MLC Bank A 48V",
                "expected_range": (-50, -46),
                "critical_range": (-52, -44),
            },
            "MLC_ADC_CHAN_M48V_BANKB_MON_STAT": {
                "patterns": [
                    "MLC_ADC_CHAN_M48V_BANKB_MON_STAT",
                    "mlc_adc_chan_m48v_bankb_mon_stat",
                    "MLC ADC CHAN M48V BANKB MON STAT",
                ],
                "unit": "V",
                "description": "MLC Bank B 48V",
                "expected_range": (-50, -46),
                "critical_range": (-52, -44),
            },
            "MLC_ADC_CHAN_5V_BANKA_MON_STAT": {
                "patterns": [
                    "MLC_ADC_CHAN_5V_BANKA_MON_STAT",
                    "mlc_adc_chan_5v_banka_mon_stat",
                    "MLC ADC CHAN 5V BANKA MON STAT",
                ],
                "unit": "V",
                "description": "MLC Bank A 5V",
                "expected_range": (4.5, 5.5),
                "critical_range": (4.0, 6.0),
            },
            "MLC_ADC_CHAN_5V_BANKB_MON_STAT": {
                "patterns": [
                    "MLC_ADC_CHAN_5V_BANKB_MON_STAT",
                    "mlc_adc_chan_5v_bankb_mon_stat",
                    "MLC ADC CHAN 5V BANKB MON STAT",
                ],
                "unit": "V",
                "description": "MLC Bank B 5V",
                "expected_range": (4.5, 5.5),
                "critical_range": (4.0, 6.0),
            },
            "MLC_ADC_CHAN_TEMP_BANKA_STAT_TEMP": {
                "patterns": [
                    "MLC_ADC_CHAN_TEMP_BANKA_STAT_TEMP",
                    "mlc_adc_chan_temp_banka_stat_temp",
                    "MLC ADC CHAN TEMP BANKA STAT TEMP",
                ],
                "unit": "°C",
                "description": "Temp MLC Bank A",
                "expected_range": (15, 35),
                "critical_range": (10, 45),
            },
            "MLC_ADC_CHAN_TEMP_BANKB_STAT_TEMP": {
                "patterns": [
                    "MLC_ADC_CHAN_TEMP_BANKB_STAT_TEMP",
                    "mlc_adc_chan_temp_bankb_stat_temp",
                    "MLC ADC CHAN TEMP BANKB STAT TEMP",
                ],
                "unit": "°C", 
                "description": "Temp MLC Bank B",
                "expected_range": (15, 35),
                "critical_range": (10, 45),
            },
            "MLC_ADC_CHAN_DISTAL_10V_BANKB_MON_STAT": {
                "patterns": [
                    "MLC_ADC_CHAN_DISTAL_10V_BANKB_MON_STAT",
                    "mlc_adc_chan_distal_10v_bankb_mon_stat",
                    "MLC ADC CHAN DISTAL 10V BANKB MON STAT",
                ],
                "unit": "V",
                "description": "MLC DISTAL 10V",
                "expected_range": (9, 11),
                "critical_range": (8, 12),
            },
            "MLC_ADC_CHAN_PROXIMAL_10V_BANKB_MON_STAT": {
                "patterns": [
                    "MLC_ADC_CHAN_PROXIMAL_10V_BANKB_MON_STAT",
                    "mlc_adc_chan_proximal_10v_bankb_mon_stat",
                    "MLC ADC CHAN PROXIMAL 10V BANKB MON STAT",
                ],
                "unit": "V",
                "description": "MLC PROXIMAL 10V",
                "expected_range": (9, 11),
                "critical_range": (8, 12),
            },
            "MotorPwr48V_Statistics": {
                "patterns": [
                    "MotorPwr48V_Statistics",
                    "motorpwr48v_statistics",
                    "Motor Pwr 48V Statistics",
                    "motorPwr48V",
                ],
                "unit": "V",
                "description": "Motor PWR 48V",
                "expected_range": (46, 50),
                "critical_range": (44, 52),
            },
            "MotorPwrN48V_Statistics": {
                "patterns": [
                    "MotorPwrN48V_Statistics",
                    "motorpwrn48v_statistics",
                    "Motor Pwr N48V Statistics",
                    "motorPwrN48V",
                ],
                "unit": "V",
                "description": "Motor PWR -48V",
                "expected_range": (-50, -46),
                "critical_range": (-52, -44),
            },
            "FanhumidityStatistics": {
                "patterns": [
                    "FanhumidityStatistics",
                    "fanhumiditystatistics",
                    "Fan humidity Statistics",
                    "humidityStatistics",
                ],
                "unit": "%",
                "description": "Room Humidity",
                "expected_range": (40, 60),
                "critical_range": (30, 80),
            },
            "COL_BOARD_TEMP_MON_STAT": {
                "patterns": [
                    "COL_BOARD_TEMP_MON_STAT",
                    "col_board_temp_mon_stat",
                    "COL BOARD TEMP MON STAT",
                ],
                "unit": "°C",
                "description": "Temp COL Board",
                "expected_range": (20, 40),
                "critical_range": (15, 50),
            },
            "magnetronTemp": {
                "patterns": [
                    "magnetronTemp",
                    "magnetron_temp",
                    "Magnetron Temp",
                    "magnetron temperature",
                ],
                "unit": "°C",
                "description": "Temp Magnetron",
                "expected_range": (30, 60),
                "critical_range": (25, 80),
            },
            "CoolingWaterTankTempStatistics": {
                "patterns": [
                    "CoolingWaterTankTempStatistics",
                    "coolingwatertanktempstatistics",
                    "Cooling Water Tank Temp Statistics",
                    "waterTankTemp",
                ],
                "unit": "°C",
                "description": "Temp Water Tank",
                "expected_range": (15, 25),
                "critical_range": (10, 35),
            },
        }

        # Create reverse mapping for quick lookup
        self.pattern_to_unified = {}
        for unified_name, config in self.parameter_mapping.items():
            for pattern in config["patterns"]:
                key = pattern.lower().replace(" ", "").replace(":", "")
                self.pattern_to_unified[key] = unified_name

    def parse_file_chunked(
        self,
        file_path: str,
        chunk_size: int = 1000,
        progress_callback=None,
        cancel_callback=None,
    ) -> pd.DataFrame:
        """Parse LINAC log file with chunked processing for large files"""
        start_time = datetime.now()
        self.parsing_stats = {
            "lines_processed": 0,
            "records_extracted": 0,
            "errors_encountered": 0,
            "processing_time": 0,
            "file_size": 0,
        }

        try:
            # Get file size for progress tracking
            self.parsing_stats["file_size"] = os.path.getsize(file_path)

            all_records = []

            with open(file_path, "r", encoding="utf-8", errors="replace") as file:
                chunk_lines = []
                total_lines = 0

                # First pass: count total lines for progress tracking
                if progress_callback:
                    file.seek(0)
                    total_lines = sum(1 for _ in file)
                    file.seek(0)

                for line_num, line in enumerate(file, 1):
                    # Check for cancellation
                    if cancel_callback and cancel_callback():
                        return pd.DataFrame()

                    chunk_lines.append((line_num, line))

                    # Process chunk when it's full or at end of file
                    if len(chunk_lines) >= chunk_size:
                        chunk_records = self._process_chunk(chunk_lines)
                        all_records.extend(chunk_records)
                        chunk_lines = []

                        # Update progress
                        if progress_callback:
                            progress = (
                                (line_num / total_lines) * 100 if total_lines > 0 else 0
                            )
                            progress_callback(
                                progress,
                                f"Processing line {line_num:,} of {total_lines:,}",
                            )

                # Process remaining lines
                if chunk_lines:
                    chunk_records = self._process_chunk(chunk_lines)
                    all_records.extend(chunk_records)

            # Create DataFrame from all records
            if all_records:
                result_df = pd.DataFrame(all_records)
                result_df = self._clean_and_validate_data(result_df)
            else:
                result_df = pd.DataFrame()

        except Exception as e:
            print(f"Error parsing file {file_path}: {e}")
            result_df = pd.DataFrame()
            self.parsing_stats["errors_encountered"] += 1

        # Calculate processing time
        end_time = datetime.now()
        self.parsing_stats["processing_time"] = (end_time - start_time).total_seconds()

        return result_df

    def _process_chunk(self, chunk_lines: List[Tuple[int, str]]) -> List[Dict]:
        """Process a chunk of lines"""
        chunk_records = []

        for line_num, line in chunk_lines:
            self.parsing_stats["lines_processed"] += 1

            try:
                line_records = self._parse_line_enhanced(line, line_num)
                chunk_records.extend(line_records)
                self.parsing_stats["records_extracted"] += len(line_records)
            except Exception as e:
                self.parsing_stats["errors_encountered"] += 1
                continue

        return chunk_records

    def _parse_line_enhanced(self, line: str, line_number: int) -> List[Dict]:
        """Enhanced line parsing with unified parameter mapping"""
        records = []

        # Extract datetime
        datetime_str = self._extract_datetime(line)
        if not datetime_str:
            return records

        # Extract serial number
        serial_number = self._extract_serial_number(line)

        # Enhanced parameter extraction with unified mapping
        match = self.patterns["water_parameters"].search(line)
        if match:
            try:
                param_raw = match.group(1).strip()
                count_val = int(match.group(2))
                max_val = float(match.group(3))
                min_val = float(match.group(4))
                avg_val = float(match.group(5))

                # Map to unified parameter name
                param_clean = param_raw.lower().replace(" ", "").replace(":", "")
                unified_param = self.pattern_to_unified.get(param_clean)

                if unified_param and self._validate_parameter_values(
                    unified_param, max_val, min_val, avg_val
                ):
                    config = self.parameter_mapping[unified_param]

                    # Create records for max, min, avg
                    for stat_type, value in [
                        ("max", max_val),
                        ("min", min_val),
                        ("avg", avg_val),
                    ]:
                        record = {
                            "line_number": line_number,
                            "datetime": datetime_str,
                            "serial_number": serial_number,
                            "parameter_type": unified_param,
                            "statistic_type": stat_type,
                            "value": value,
                            "count": count_val,
                            "unit": config["unit"],
                            "description": config["description"],
                            "data_quality": self._assess_data_quality(
                                unified_param, value, count_val
                            ),
                            "raw_parameter": param_raw,
                        }
                        records.append(record)

            except (ValueError, IndexError) as e:
                self.parsing_stats["errors_encountered"] += 1

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
        """Extract serial number with multiple pattern support"""
        for pattern_name in ["serial_number", "serial_alt", "machine_id"]:
            if pattern_name in self.patterns:
                match = self.patterns[pattern_name].search(line)
                if match:
                    serial_raw = match.group(1)
                    return f"SN#{int(serial_raw)}"

        return "Unknown"

    def _validate_parameter_values(
        self, param_name: str, max_val: float, min_val: float, avg_val: float
    ) -> bool:
        """Enhanced parameter value validation with unified mapping"""
        if param_name not in self.parameter_mapping:
            return True  # Allow unknown parameters

        config = self.parameter_mapping[param_name]
        critical_min, critical_max = config["critical_range"]

        # Basic logical validation
        if not (min_val <= avg_val <= max_val):
            return False

        # Range validation with tolerance
        tolerance_factor = 2.0
        extended_min = critical_min - (critical_max - critical_min) * tolerance_factor
        extended_max = critical_max + (critical_max - critical_min) * tolerance_factor

        if not (
            extended_min <= min_val <= extended_max
            and extended_min <= max_val <= extended_max
        ):
            return False

        # Check for reasonable variance
        value_range = max_val - min_val
        if value_range > avg_val * 0.5 and avg_val > 0:
            return False

        return True

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

    def get_parsing_stats(self) -> Dict:
        """Get parsing statistics"""
        return self.parsing_stats.copy()

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
