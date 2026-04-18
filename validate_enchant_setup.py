#!/usr/bin/env python3
"""
Validation script for enchant architecture setup.
Checks that all required directories and binaries exist.
Supports: enchant_x86, enchant_x64, enchant_aarch64
"""

import os
import platform
from enchant_architecture import EnchantArchitecture

def validate():
    detected = EnchantArchitecture()
    print(f"✓ Detected architecture: {detected}")
    
    # Check required directories
    dirs_to_check = [
        f"{detected}/data/bin",
        f"{detected}/data/lib/enchant-2",
    ]
    
    all_ok = True
    for dir_path in dirs_to_check:
        if os.path.isdir(dir_path):
            files = os.listdir(dir_path)
            print(f"✓ {dir_path}/ exists ({len(files)} files)")
        else:
            print(f"✗ {dir_path}/ NOT FOUND")
            all_ok = False
    
    # Define critical DLLs by architecture
    if detected == "enchant_aarch64":
        critical_dlls = [
            "libenchant-2-2.dll",      # ARM64 uses libenchant-2-2
            "libhunspell-1.7-0.dll",   # ARM64 uses 1.7
        ]
        print(f"\n[ARM64 Mode] Checking for ARM64-specific DLL names...")
    elif detected == "enchant_x64":
        critical_dlls = [
            "libenchant-2.dll",        # x64 uses libenchant-2
            "libhunspell-1.6-0.dll",   # x64 uses 1.6
        ]
        print(f"\n[x64 Mode] Checking for x64-specific DLL names...")
    else:  # enchant_x86
        critical_dlls = [
            "libenchant-2.dll",        # x86 uses libenchant-2
            "libhunspell-1.6-0.dll",   # x86 uses 1.6
        ]
        print(f"\n[x86 Mode] Checking for x86-specific DLL names...")
    
    # Check for critical binaries
    bin_path = f"{detected}/data/bin"
    for dll in critical_dlls:
        full_path = os.path.join(bin_path, dll)
        if os.path.exists(full_path):
            size_kb = os.path.getsize(full_path) / 1024
            print(f"✓ {dll} ({size_kb:.1f} KB)")
        else:
            print(f"✗ {dll} MISSING")
            all_ok = False
    
    # Check for hunspell backend plugin
    lib_path = f"{detected}/data/lib/enchant-2"
    hunspell_plugin = os.path.join(lib_path, "enchant_hunspell.dll")
    if os.path.exists(hunspell_plugin):
        size_kb = os.path.getsize(hunspell_plugin) / 1024
        print(f"✓ enchant_hunspell.dll ({size_kb:.1f} KB)")
    else:
        print(f"✗ enchant_hunspell.dll MISSING")
        all_ok = False
    
    print()

    # Check required Python files in enchant_aarch64/
    required_py_files = [
        "__init__.py",
        "_enchant.py",
        "errors.py",
        "utils.py",
        "pypwl.py",
    ]
    print(f"[Checking {detected} Python files]")
    for fname in required_py_files:
        fpath = os.path.join(detected, fname)
        if os.path.exists(fpath):
            print(f"[PASS] {detected}/{fname} found")
        else:
            print(f"[FAIL] {detected}/{fname} MISSING")
            all_ok = False

    print()
    if all_ok:
        print("✓ All validation checks passed!")
        return True
    else:
        print("✗ Some files are missing. Please check:")
        print(f"   - Architecture detected: {detected}")
        print(f"   - Required DLL names for {detected}:")
        for dll in critical_dlls:
            print(f"     • {dll}")
        print(f"\n   If you have different DLL versions, update this script.")
        return False

if __name__ == "__main__":
    import sys
    sys.exit(0 if validate() else 1)