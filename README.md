# CUDA Spell Checker

A spell-checking plugin for [CudaText](https://cudatext.github.io/) that highlights misspelled words with red underlines and offers correction suggestions in real time.

Powered by [Enchant](https://abiword.github.io/enchant/) and [Hunspell](https://hunspell.github.io/) dictionaries. On Windows, all required binaries are bundled — no extra installation needed.

## Features

- Real-time underline highlighting of misspelled words
- Correction suggestions dialog (Ignore / Change / Add to dictionary / Cancel)
- Smart filtering to reduce false positives in source code:
  - `ALL_CAPS` words (constants)
  - `camelCase` and `MixedCase` identifiers
  - Words containing numbers (e.g. `v1.0`)
  - Words containing underscores (`snake_case`)
  - URLs (configurable regex)
- Lexer-aware: when a syntax lexer is active, only comments and strings are checked
- Persistent JSON cache for fast subsequent checks (survives editor restarts)
- Automatic cache invalidation when Hunspell dictionary files change
- Multi-language support via selectable dictionaries
- Navigate to next/previous misspelled word
- List all misspelled words in a new tab
- Event-driven checking: on file open and/or while editing (after a configurable pause)

## Requirements

- [CudaText](https://cudatext.github.io/) text editor

**Windows:** all Enchant/Hunspell binaries are bundled — nothing extra to install.

**Linux/macOS:** install the system Enchant and Hunspell packages, e.g.:
```bash
# Debian/Ubuntu
sudo apt-get install enchant-2 hunspell

# macOS (Homebrew)
brew install enchant
```

## Installation

**Via CudaText** (recommended): open `Plugins → Addon Manager → Install` and search for "Spell Checker".

**Manual**: copy the `cuda_spell_checker/` folder into CudaText's `py/` plugins directory and restart the editor.

## Platform Support

The plugin automatically detects your architecture at runtime and loads the correct binaries — no manual configuration needed.

| Platform | Architecture     | Status    |
|----------|------------------|-----------|
| Windows  | 32-bit x86       | Supported |
| Windows  | 64-bit x86-64    | Supported |
| Windows  | 64-bit ARM64     | Supported |
| Linux    | any              | Supported (system Enchant) |
| macOS    | any              | Supported (system Enchant) |

### Windows ARM64

Native ARM64 support was added to avoid running through x86 emulation on ARM-based Windows devices (e.g. Snapdragon X laptops, Surface Pro X). The ARM64 build ships Hunspell 1.7 with ARM64-native DLLs compiled via LLVM/clang on MSYS2.

Detection is done automatically using `sys.maxsize` (bitness) and `platform.machine()` (CPU family). See [`enchant_architecture.py`](enchant_architecture.py) for the detection logic and [`ARCHITECTURE_SUPPORT.md`](ARCHITECTURE_SUPPORT.md) for details on adding further architectures.

## Additional Dictionaries

The plugin ships with `en_US` and `de_DE` dictionaries on Windows. To add more languages, download a Hunspell dictionary (`.dic` + `.aff` files) and copy them to:

| Platform | Path |
|----------|------|
| Windows 32-bit | `CudaText\py\cuda_spell_checker\enchant_x86\data\share\enchant\hunspell\` |
| Windows 64-bit | `CudaText\py\cuda_spell_checker\enchant_x64\data\share\enchant\hunspell\` |
| Windows ARM64  | `CudaText\py\cuda_spell_checker\enchant_aarch64\data\share\enchant\hunspell\` |
| Linux/Unix     | `~/.enchant/myspell` or `~/.config/enchant` |

Rename files to a short locale code without spaces (e.g. `Russian.*` → `ru_RU.*`).

Dictionary sources:
- https://github.com/titoBouzout/Dictionaries
- https://github.com/wooorm/dictionaries
- https://addons.mozilla.org/en-US/firefox/language-tools/
- https://extensions.libreoffice.org/
- http://app.aspell.net/create (English)
- https://sourceforge.net/projects/wordlist/

Then use **Plugins → Spell Checker → Select language** to activate the new dictionary.

## Menu Commands

| Menu item | Description |
|-----------|-------------|
| Check text | Check full document (or selection) |
| Check text, with suggestions | Same, with suggestion dialog per misspelled word |
| Check word | Check word under caret |
| Check word, with suggestions | Same, with suggestion dialog |
| Go to next/previous misspelled | Navigate between highlighted words |
| Create a list with all misspelled words | Open a new tab with sorted unique misspelled words |
| Select language | Choose installed dictionary |
| Configure | Edit settings INI file |
| Configure events | Toggle auto-check on open / while editing |

## Configuration

Settings are stored in `cuda_spell_checker.ini`. Open via **Options → Settings-plugins → Spell Checker → Configure**.

| Option | Default | Description |
|--------|---------|-------------|
| `lang` | `en_US` | Active dictionary language |
| `underline_style` | — | Underline style (0–6) |
| `confirm_esc_key` | `1` | Show confirmation when Esc is pressed during checking |
| `file_extension_list` | — | Extensions for auto-checking (`*` = all, `txt,md` = listed, empty = disabled) |
| `url_regex` | — | Regex pattern for URLs to skip |
| `cache_lifetime` | `60` | Cache TTL in minutes (`0` = keep forever until dictionary changes) |

## Personal Word List

Words added via the **Add** button are saved to a personal dictionary:

- **Windows:** `C:\Users\<username>\AppData\Local\enchant\*.dic`
- **Linux/macOS:** `~/.config/enchant/*.dic`

## Authors

- Alexey Torgashin (CudaText)
- Andreas Heim — Enchant Windows DLL support
- CudaText forum member A:C — major refactoring
- Badr Elmers — performance improvements and refactoring

## License

MIT
