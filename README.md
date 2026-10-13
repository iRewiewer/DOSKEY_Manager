# DOSKEY Manager

DOSKEY Manager is a small Windows CMD / Windows Terminal startup utility. It loads DOSKEY aliases from JSON profiles, optionally prints a randomized welcome screen, and can rotate the Windows Terminal background on every interactive CMD session.

## Requirements

- Windows
- Python available as `python`
- Windows Terminal, if you want background rotation

## Setup

Run:

```bat
setup.bat
```

By default, setup installs the AutoRun hook under the current user:

```text
HKCU\Software\Microsoft\Command Processor\AutoRun
```

The old machine-wide `HKLM` mode is no longer needed for normal use.

## Commands

After setup, open a new CMD / Windows Terminal session and use:

```bat
d help
d status
d aliases
d bg
d bg blue
d disable
d enable
d uninstall
```

The command prefix defaults to `d`. Change `commandPrefix` in `config.json` if you want a different command prefix. The prefix cannot be empty and cannot contain whitespace or `=`.

Legacy aliases such as `hcfg`, `helpcfg`, `cfg`, and `version` are still provided by the core profile.

## Profiles

Profiles live in the `profiles` folder. Each JSON file is one profile:

```json
{
    "name": "example",
    "description": "Example aliases",
    "aliases": [
        {
            "name": "projects",
            "command": "cd /d \"C:\\Path\\To\\Projects\"",
            "help": "Jump to a local projects folder."
        }
    ]
}
```

Load order is controlled by `profiles.json`. Files listed there load first. Any other `*.json` file in `profiles` is discovered automatically and loaded afterward.

Profile files whose names start with `_` or `.` are ignored on purpose. This lets the repository ship examples beside the real profiles without loading them.

Alias names and commands can use placeholders such as `{app}`, `{profiles}`, `{loader}`, `{manager}`, `{notepad}`, and `{commandPrefix}`.

This makes private profiles easy:

1. Create `profiles/my-local-profile.local.json`.
2. Keep machine-specific paths and private aliases in that file.
3. Do not add it to `profiles.json`; it will still load automatically.

Reference profiles that should not autoload can stay in `profiles` with an ignored prefix, such as `profiles/_doskey-examples.json`.

## Folder Layout

```text
assets/
  backgrounds/          Windows Terminal background images
  welcome_screens/      Startup text templates
profiles/               Loaded alias profiles
  _doskey-examples.json Ignored reference profile
src/
  doskey_manager.py     CLI entrypoint used by DOSKEY_Loader.bat
  doskey_manager_app/   Implementation modules
tools/                  Helper scripts
config.json             App settings
profiles.json           Public profile load order
DOSKEY_Loader.bat       AutoRun loader and command entrypoint
setup.bat               Install current-user AutoRun
disable.bat             Soft-disable startup behavior
uninstall.bat           Remove current-user AutoRun
```

## Backgrounds

Background images are grouped by folder under `assets/backgrounds`.

```bat
d bg
d bg red
d bg green
```

`d bg` chooses a random image. `d bg <folder>` chooses a random image from that background group. Supported image extensions include GIF, PNG, JPG, JPEG, WEBP, and BMP.

Startup background rotation runs asynchronously by default so the prompt becomes usable faster. In `config.json`, `startup.backgroundMode` accepts:

- `async`: update the Windows Terminal background after aliases load
- `sync`: update the background before the prompt, matching the old blocking behavior
- `off`: skip automatic background updates

Before changing Windows Terminal settings, DOSKEY Manager writes backups under `backups`.

## Welcome Screens

Welcome screens live under `assets/welcome_screens`. Only files inside `assets/welcome_screens/active` are candidates for startup display.

Templates support random placeholders:

```text
%_random_d_6_%
%_random_dmc_12_%
```

Supported placeholder modes:

- `d`: digits
- `sc`: lowercase letters
- `bc`: uppercase letters
- `mc`: mixed letters
- `dsc`: digits and lowercase letters
- `dbc`: digits and uppercase letters
- `dmc`: digits and mixed letters

## Disable vs Uninstall

`d disable` creates a local marker file and makes startup return silently, while keeping the command entrypoint available. This is useful when another program is confused by AutoRun output.

```bat
d disable
d enable
```

`d disable --hard` removes the user AutoRun hook. `d uninstall` also removes the hook.

```bat
d disable --hard
d uninstall
```

## Notes

Some software launches `cmd.exe` internally and can break if AutoRun prints text or changes terminal settings. DOSKEY Manager skips startup behavior for `cmd /c` calls, which should avoid most of those cases while preserving normal interactive startup behavior.

## Changelog

### v3.0

- Added JSON profile loading from `profiles`.
- Added configurable command prefixes through `commandPrefix`.
- Moved startup background rotation to async mode by default.
- Added `profiles.json` load order with automatic discovery for unlisted profile files.
- Added ignored profile filenames using `_` or `.` prefixes.
- Split the Python implementation into focused modules under `src/doskey_manager_app`.
- Split source, assets, tools, profiles, and backups into separate folders.
- Folded command dispatch into `DOSKEY_Loader.bat`; removed the separate manager wrapper.
- Switched setup to current-user AutoRun by default.
- Added soft-disable mode.
- Added lock-protected Windows Terminal settings writes and backup rotation.

### v2.4

- Added `disable-cfg`.
- Added `uninstall.bat`.

### v2.3

- Added random title display.

### v2.2

- Added config support for a custom Windows Terminal package path.
- Reworked file loading.

### v2.1

- Added background folder detection for `bg -type <folder>`.

### v2.0

- Added `version`.
- Added Linux-like aliases.
- Added Windows Terminal background changing.
- Streamlined installation.

### v1.x

- Initial alias loader, welcome text, color help, and Notepad++ detection.
