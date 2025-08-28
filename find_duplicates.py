#!/usr/bin/env python3
"""Find duplicate patterns in parser_linac.py"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser_linac import LinacParser

parser = LinacParser()

all_patterns = {}
duplicates = []

for param_key, config in parser.parameter_mapping.items():
    for pattern in config["patterns"]:
        normalized_pattern = pattern.lower().replace(" ", "").replace(":", "")
        if normalized_pattern in all_patterns:
            print(f"DUPLICATE: '{pattern}' (normalized: '{normalized_pattern}')")
            print(f"  Already in parameter: {all_patterns[normalized_pattern]}")
            print(f"  Also found in parameter: {param_key}")
            print()
        else:
            all_patterns[normalized_pattern] = param_key

print(f"Total patterns: {len(all_patterns)}")