import sys
import platform
import os

def EnchantArchitecture():
    """
    Detect the current system architecture and return the appropriate
    enchant subdirectory name.
    
    Returns:
        str: One of 'enchant_x86', 'enchant_x64', or 'enchant_aarch64'
    """
    
    if sys.maxsize > 2**32:  # 64-bit Python
        machine = platform.machine().lower()
        
        if 'arm64' in machine or 'aarch64' in machine:
            return 'enchant_aarch64'
        else:
            return 'enchant_x64'
    else:
        return 'enchant_x86'


def GetEnchantLibName():
    """
    Handle potential naming variations of libenchant across versions.
    Returns the DLL name that exists in the current arch's bin/ folder.
    
    Returns:
        str: Either 'libenchant-2' or 'libenchant-2-2' (without .dll)
    """
    arch = EnchantArchitecture()
    bin_path = os.path.join(os.path.dirname(__file__), arch, 'data', 'bin')
    
    # Check for both possible names
    for name in ['libenchant-2-2.dll', 'libenchant-2.dll']:
        full_path = os.path.join(bin_path, name)
        if os.path.exists(full_path):
            return name.replace('.dll', '')
    
    # Default fallback
    return 'libenchant-2'