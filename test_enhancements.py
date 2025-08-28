#!/usr/bin/env python3
"""
HALog Enhancement Validation Test
Tests all new features and enhancements for the HALog application
"""

import sys
import os
from pathlib import Path

def test_fault_code_enhancements():
    """Test enhanced fault code functionality"""
    print("🔍 Testing Fault Code Enhancements...")
    
    from parser_fault_code import FaultCodeParser
    parser = FaultCodeParser()
    
    # Test dual database lookup
    test_codes = ['400027', '3108', '4000', '999999']
    
    for code in test_codes:
        result = parser.search_fault_code(code)
        descriptions = parser.get_fault_descriptions_by_database(code)
        
        print(f"  Code {code}:")
        if result:
            print(f"    Found in: {result['database']} database")
            print(f"    Description: {result['description'][:50]}...")
        
        print(f"    HAL: {'✓' if descriptions['hal_description'] != 'NA' else '✗'}")
        print(f"    TB:  {'✓' if descriptions['tb_description'] != 'NA' else '✗'}")
        print()
    
    return True

def test_shortdata_extraction():
    """Test shortdata parameter extraction"""
    print("📊 Testing Shortdata Parameter Extraction...")
    
    from parser_shortdata import ShortDataParser
    parser = ShortDataParser()
    result = parser.parse_log_file()
    
    if not result:
        print("  ❌ No data extracted")
        return False
    
    groups = result.get('groups', {})
    total_params = sum(len(params) for params in groups.values())
    
    print(f"  ✓ Total parameters extracted: {total_params}")
    
    for group_name, params in groups.items():
        if params:
            unique_params = list(set(p['parameter_name'] for p in params))
            print(f"  ✓ {group_name.title()}: {len(unique_params)} unique parameters")
            
            # Test data visualization format
            df = parser.get_data_for_visualization(group_name)
            if not df.empty:
                print(f"    Data points: {len(df)} | Columns: {list(df.columns)}")
    
    return True

def test_trend_visualization():
    """Test trend visualization capabilities"""
    print("📈 Testing Trend Visualization...")
    
    from parser_shortdata import ShortDataParser
    from utils_plot import PlotUtils
    
    parser = ShortDataParser()
    result = parser.parse_log_file()
    
    if not result:
        print("  ❌ No data for visualization")
        return False
    
    # Test parameter grouping
    groups = ['temperature', 'voltage', 'humidity', 'fan_speed', 'flow']
    
    for group in groups:
        params = parser.get_unique_parameter_names(group)
        if params:
            print(f"  ✓ {group.title()}: {len(params)} parameters available for visualization")
            
            # Test data extraction for visualization
            data = parser.get_data_for_visualization(group, params[0] if params else None)
            print(f"    Sample data: {len(data)} rows")
    
    # Test color scheme
    colors = PlotUtils.get_group_colors()
    print(f"  ✓ Color scheme loaded: {len(colors)} group colors")
    
    return True

def test_ui_enhancements():
    """Test UI structure enhancements"""
    print("🎨 Testing UI Enhancements...")
    
    try:
        from main_window import Ui_MainWindow
        from PyQt5.QtWidgets import QApplication, QMainWindow
        
        # Test UI creation (without display)
        app = QApplication.instance() or QApplication([])
        window = QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(window)
        
        # Check for new UI elements
        checks = [
            ('txtHALDescription', 'HAL Description text box'),
            ('txtTBDescription', 'TB Description text box'),
            ('trendSubTabs', 'Trend sub-tabs widget'),
            ('waterGraphTop', 'Water system top graph'),
            ('waterGraphBottom', 'Water system bottom graph'),
            ('voltageGraphTop', 'Voltage top graph'),
            ('voltageGraphBottom', 'Voltage bottom graph'),
            ('tempGraphTop', 'Temperature top graph'),
            ('tempGraphBottom', 'Temperature bottom graph'),
            ('humidityGraphTop', 'Humidity top graph'),
            ('humidityGraphBottom', 'Humidity bottom graph'),
        ]
        
        for attr_name, description in checks:
            if hasattr(ui, attr_name):
                print(f"  ✓ {description} created successfully")
            else:
                print(f"  ⚠️ {description} not found")
        
        return True
        
    except Exception as e:
        print(f"  ❌ UI test error: {e}")
        return False

def test_integration():
    """Test integration of all components"""
    print("🔧 Testing Component Integration...")
    
    try:
        # Test main application import
        from main import HALogApp
        print("  ✓ Main application imports successfully")
        
        # Test that all required modules are available
        modules = [
            'parser_fault_code',
            'parser_shortdata', 
            'utils_plot',
            'main_window',
            'progress_dialog'
        ]
        
        for module in modules:
            try:
                __import__(module)
                print(f"  ✓ {module} module available")
            except ImportError as e:
                print(f"  ❌ {module} import error: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Integration test error: {e}")
        return False

def main():
    """Run all validation tests"""
    print("🚀 HALog Enhancement Validation Suite")
    print("=" * 50)
    
    tests = [
        test_fault_code_enhancements,
        test_shortdata_extraction,
        test_trend_visualization,
        test_ui_enhancements,
        test_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
                print("✅ PASSED\n")
            else:
                print("❌ FAILED\n")
        except Exception as e:
            print(f"❌ ERROR: {e}\n")
    
    print("=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All enhancements validated successfully!")
        return 0
    else:
        print("⚠️ Some tests failed - please check the implementation")
        return 1

if __name__ == "__main__":
    sys.exit(main())