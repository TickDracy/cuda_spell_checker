# Enchant Architecture Support

This plugin supports CudaText spell-checking on multiple Windows architectures via different enchant binary sets.

## Supported Architectures

- **32-bit Windows (x86)**: enchant_x86/ directory
  - Detection: 32-bit Python
  - Enchant Library: libenchant-2.dll
  - Hunspell Engine: libhunspell-1.6-0.dll
  - DLL Exception Model: DW2
  - Status: Supported

- **64-bit Windows x86-64 (AMD64)**: enchant_x64/ directory
  - Detection: 64-bit Python + x86_64 CPU
  - Enchant Library: libenchant-2.dll
  - Hunspell Engine: libhunspell-1.6-0.dll
  - DLL Exception Model: SEH
  - Status: Supported

- **64-bit Windows ARM64 (aarch64)**: enchant_aarch64/ directory
  - Detection: 64-bit Python + arm64/aarch64 CPU
  - Enchant Library: libenchant-2-2.dll (ARM64 build)
  - Hunspell Engine: libhunspell-1.7-0.dll (ARM64 build)
  - DLL Exception Model: ARM64-specific
  - Status: Supported (NEW)
  - Note: `libgobject-2.0-0.dll` is intentionally absent — it is a GLib dependency of the x64 MinGW build only. The ARM64 enchant build does not require it, and no code in this plugin references libgobject directly.

## How It Works

### Architecture Detection

The plugin automatically detects the running system's architecture using:

1. Bitness detection: `sys.maxsize > 2**32` (32-bit vs 64-bit)
2. CPU detection: `platform.machine()` (x86_64 vs arm64/aarch64)

This mapping is done in `enchant_architecture.py`.

### Binary Loading

When the plugin loads:

1. `EnchantArchitecture()` returns the correct subdirectory name
2. The main `__init__.py` uses dynamic imports to load from that directory
3. All dependent modules (checker, tokenize, etc.) use the same detection mechanism
4. DLLs are loaded from `{arch}/data/bin/` via PATH environment variable
5. The Enchant backend plugin (`enchant_hunspell.dll`) is loaded from `{arch}/data/lib/enchant-2/`

## Adding a New Architecture

To support a new architecture:

1. Create a new directory: `enchant_newarch/`

2. Mirror the structure of `enchant_x64/`:

   ```
   enchant_newarch/
   ├── data/
   │   ├── bin/          (put DLLs here)
   │   └── lib/enchant-2/
   ├── checker/
   ├── tokenize/
   └── __init__.py
   ```

3. Copy Python modules from `enchant_x64/` to `enchant_newarch/`

4. Update `enchant_architecture.py` to return the new directory name when detected

5. Place the pre-compiled enchant binaries in `data/bin/` and `data/lib/enchant-2/`

## Validation

Run the validation script to check your setup:

```bash
python validate_enchant_setup.py
```

Expected output for **x86/x64** when successful:

```
✓ Detected architecture: enchant_x64
✓ enchant_x64/data/bin/ exists (21 files)
✓ enchant_x64/data/lib/enchant-2/ exists (1 files)
✓ libenchant-2.dll (2048.3 KB)
✓ libhunspell-1.6-0.dll (812.5 KB)
✓ enchant_hunspell.dll (37.5 KB)

✓ All validation checks passed!
```

Expected output for **ARM64** when successful:

```
✓ Detected architecture: enchant_aarch64
✓ enchant_aarch64/data/bin/ exists (23 files)
✓ enchant_aarch64/data/lib/enchant-2/ exists (4 files)
[ARM64 Mode] Checking for ARM64-specific DLL names...
✓ libenchant-2-2.dll (82.5 KB)
✓ libhunspell-1.7-0.dll (793.5 KB)
✓ enchant_hunspell.dll (37.5 KB)

✓ All validation checks passed!
```

## Directory Structure Reference

Complete structure with all architectures:

```
cuda_spell_checker/
├── enchant_x86/
│   ├── data/
│   │   ├── bin/          (32-bit DLLs)
│   │   └── lib/enchant-2/
│   ├── checker/
│   ├── tokenize/
│   └── __init__.py
├── enchant_x64/
│   ├── data/
│   │   ├── bin/          (64-bit AMD64 DLLs)
│   │   └── lib/enchant-2/
│   ├── checker/
│   ├── tokenize/
│   └── __init__.py
├── enchant_aarch64/
│   ├── data/
│   │   ├── bin/          (64-bit ARM64 DLLs)
│   │   └── lib/enchant-2/
│   ├── checker/
│   ├── tokenize/
│   └── __init__.py
├── enchant_architecture.py
├── validate_enchant_setup.py
├── ARCHITECTURE_SUPPORT.md
└── __init__.py
```

## Important Notes

- **All Python modules** (checker, tokenize, utils, errors) are **identical** across architectures
- **Only the DLL binaries differ** by architecture
- **Architecture detection is automatic** — no manual configuration needed
- **DLL names differ by architecture:**
  - x86/x64: Uses `libenchant-2.dll` and `libhunspell-1.6-0.dll`
  - ARM64: Uses `libenchant-2-2.dll` and `libhunspell-1.7-0.dll`
- On Windows, ensure **all DLLs and their dependencies** are in the correct `data/bin/` folder
- The validation script automatically detects your architecture and checks for the correct DLL names

## Implementation Details

The `enchant_architecture.py` module provides:

- **`EnchantArchitecture()`**: Returns the architecture string (`enchant_x86`, `enchant_x64`, or `enchant_aarch64`)
- **`GetEnchantLibName()`**: Handles DLL name variations (returns `libenchant-2` or `libenchant-2-2` without extension)

Both functions are used by the plugin to dynamically load the correct binaries at runtime.
