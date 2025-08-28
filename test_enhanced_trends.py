"""
Test script to validate the enhanced parameter mapping and trend tab functionality
"""
import unittest
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser_linac import LinacParser

class TestEnhancedTrendMapping(unittest.TestCase):
    
    def setUp(self):
        self.parser = LinacParser()
    
    def test_parameter_mapping_completeness(self):
        """Test that all required parameters are mapped with correct descriptions"""
        
        required_mappings = {
            "MLC_ADC_CHAN_TEMP_BANKB_STAT_24V": "MLC Bank B 24V",
            "MLC_ADC_CHAN_TEMP_BANKA_STAT_24V": "MLC Bank A 24V", 
            "FanfanSpeed1Statistics": "Speed FAN 1",
            "FanfanSpeed2Statistics": "Speed FAN 2",
            "FanfanSpeed3Statistics": "Speed FAN 3",
            "FanfanSpeed4Statistics": "Speed FAN 4",
            "magnetronFlow": "Mag Flow",
            "cityWaterFlow": "Flow Chiller Water",
            "CoolingtargetTempStatistics": "Flow Target",
            "targetAndCirculatorFlow": "Flow Target",
            "FanremoteTempStatistics": "Temp Room",
            "pdu_boardTemp_STAT": "Temp PDU",
            "COL_ADC_CHAN_M48V_MON_STAT": "COL 48V",
            "MLC_ADC_CHAN_M48V_BANKA_MON_STAT": "MLC Bank A 48V",
            "MLC_ADC_CHAN_M48V_BANKB_MON_STAT": "MLC Bank B 48V",
            "MLC_ADC_CHAN_5V_BANKA_MON_STAT": "MLC Bank A 5V",
            "MLC_ADC_CHAN_5V_BANKB_MON_STAT": "MLC Bank B 5V",
            "MLC_ADC_CHAN_TEMP_BANKA_STAT_TEMP": "Temp MLC Bank A",
            "MLC_ADC_CHAN_TEMP_BANKB_STAT_TEMP": "Temp MLC Bank B",
            "MLC_ADC_CHAN_DISTAL_10V_BANKB_MON_STAT": "MLC DISTAL 10V",
            "MLC_ADC_CHAN_PROXIMAL_10V_BANKB_MON_STAT": "MLC PROXIMAL 10V",
            "MotorPwr48V_Statistics": "Motor PWR 48V",
            "MotorPwrN48V_Statistics": "Motor PWR -48V",
            "FanhumidityStatistics": "Room Humidity",
            "COL_BOARD_TEMP_MON_STAT": "Temp COL Board",
            "magnetronTemp": "Temp Magnetron",
            "CoolingWaterTankTempStatistics": "Temp Water Tank"
        }
        
        for param_key, expected_description in required_mappings.items():
            self.assertIn(param_key, self.parser.parameter_mapping, 
                         f"Parameter {param_key} not found in mapping")
            actual_description = self.parser.parameter_mapping[param_key]["description"]
            self.assertEqual(actual_description, expected_description,
                           f"Parameter {param_key}: expected '{expected_description}', got '{actual_description}'")
    
    def test_parameter_units(self):
        """Test that parameters have correct units"""
        unit_tests = {
            "FanfanSpeed1Statistics": "RPM",
            "magnetronFlow": "L/min", 
            "COL_ADC_CHAN_M48V_MON_STAT": "V",
            "FanremoteTempStatistics": "°C",
            "FanhumidityStatistics": "%"
        }
        
        for param_key, expected_unit in unit_tests.items():
            self.assertIn(param_key, self.parser.parameter_mapping)
            actual_unit = self.parser.parameter_mapping[param_key]["unit"]
            self.assertEqual(actual_unit, expected_unit,
                           f"Parameter {param_key}: expected unit '{expected_unit}', got '{actual_unit}'")
    
    def test_no_duplicate_patterns(self):
        """Test that there are no duplicate patterns causing conflicts between different parameters"""
        all_patterns = {}
        for param_key, config in self.parser.parameter_mapping.items():
            for pattern in config["patterns"]:
                normalized_pattern = pattern.lower().replace(" ", "").replace(":", "")
                if normalized_pattern in all_patterns:
                    existing_param = all_patterns[normalized_pattern]
                    if existing_param != param_key:  # Only fail if it's a different parameter
                        self.fail(f"Duplicate pattern found between different parameters: '{pattern}' (normalized: '{normalized_pattern}') is in both '{existing_param}' and '{param_key}'")
                else:
                    all_patterns[normalized_pattern] = param_key

class TestUIStructure(unittest.TestCase):
    """Test UI structure without actually creating the GUI"""
    
    def test_import_ui_module(self):
        """Test that the main window module can be imported"""
        try:
            from main_window import Ui_MainWindow
            self.assertTrue(True, "Successfully imported main_window module")
        except ImportError as e:
            self.fail(f"Failed to import main_window: {e}")
    
    def test_dropdown_structure(self):
        """Test that the UI has the expected dropdown structure"""
        from main_window import Ui_MainWindow
        from PyQt5.QtWidgets import QMainWindow, QApplication
        import sys
        
        # Create a minimal QApplication if one doesn't exist
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        try:
            # Create window and UI
            window = QMainWindow()
            ui = Ui_MainWindow()
            ui.setupUi(window)
            
            # Test that the new dropdown controls exist
            expected_dropdowns = [
                'comboWaterTopGraph', 'comboWaterBottomGraph',
                'comboVoltageTopGraph', 'comboVoltageBottomGraph', 
                'comboTempTopGraph', 'comboTempBottomGraph',
                'comboHumidityTopGraph', 'comboHumidityBottomGraph',
                'comboFanTopGraph', 'comboFanBottomGraph'
            ]
            
            for dropdown_name in expected_dropdowns:
                self.assertTrue(hasattr(ui, dropdown_name), 
                              f"Missing dropdown: {dropdown_name}")
                dropdown = getattr(ui, dropdown_name)
                self.assertTrue(dropdown.count() > 1, 
                              f"Dropdown {dropdown_name} should have items")
                
        except Exception as e:
            # If GUI can't be created (headless environment), just pass
            if "cannot connect to display" in str(e).lower() or "xcb" in str(e).lower():
                self.skipTest("Skipping GUI test in headless environment")
            else:
                raise e

if __name__ == "__main__":
    unittest.main()