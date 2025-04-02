# hyprkan ⌨️

**hyprkan** is a layer switcher for [kanata](https://github.com/jtroo/kanata) that works exclusively on [Hyprland](https://hyprland.org). It listens to [Hyprland events](https://wiki.hyprland.org/IPC), detects active windows, and switches the kanata layer based on window class and title using a JSON configuration.

> [!WARNING]
> Please be aware that **hyprkan** is currently in its beta version. As such, it may contain bugs that have not yet been identified or resolved.

## Table of Contents

- [Usage](#usage)
  - [hyprkan Service](#setting-up-as-a-service)
- [Configuration](#configuration)
  - [Properties](#config-properties)
  - [Example](#config-example)
- [hyprkan Options](#hyprkan-options)

## Usage

After downloading [hyprkan](/hyprkan):

1. Ensure that kanata is running and configured correctly.
2. Set your rules in the [configuration file](#configuration).
3. Now you can run hyprkan.

> [!IMPORTANT]
> Make sure hyprkan is executable:
>
> ```bash
> chmod +x hyprkan
> ```

### Setting Up as a Service

To run hyprkan automatically, you can set it up as a [systemd service](https://en.wikipedia.org/wiki/Systemd).

Create a systemd user service file at `~/.config/systemd/user/hyprkan.service` with the following content:

```ini
[Unit]
Description=Kanata Layer Switcher
After=graphical-session.target

[Service]
ExecStart=%h/.local/bin/hyprkan
Restart=on-failure
RestartSec=5
Type=simple

[Install]
WantedBy=graphical-session.target
```

> [!NOTE]
> Make sure to replace `%h/.local/bin/hyprkan` with the correct path to the hyprkan file.

1. Start the service:

   ```bash
   systemctl --user start hyprkan
   ```

2. Enable the service to start automatically on boot:

   ```bash
   systemctl --user enable hyprkan
   ```

3. Check the status of the service:
   ```bash
   systemctl --user status hyprkan
   ```

## Configuration

The configuration file is a [JSON](https://en.wikipedia.org/wiki/JSON) file where you define window rules and the corresponding kanata layers. The default configuration file is located at: `~/.config/kanata/apps.json`

### Config Properties

Here are the properties you can include in the configuration file:

- `base`: The base layer used as a fallback when no specific rule matches the current app.
- `exec`: Bash commands to execute every time the kanata layer switches.
  This can be useful if you want to send a notification when the layer changes. For example, you can use `notify-send -r 12345 'Current Layer' $CURRENT_LAYER`.
  `CURRENT_LAYER` is an environment variable you can use to get the current layer's name.
- `rules`: A set of rules that define which layer to switch to based on the active window's class or title. See [nata's window rules](https://github.com/mdSlash/nata/blob/main/docs/config.md#window_rules) for more information.

### Config Example

Here is an example structure for the configuration file:

```json
{
  "base": "BaseLayer",
  "exec": "notify-send $CURRENT_LAYER",
  "rules": [
    {
      "class": "ExampleClass",
      "title": "ExampleTitle",
      "layer": "ExampleLayer"
    }
  ]
}
```

## hyprkan Options

Here is a list of available options:

- `-h`, `--help`
  Display the help message and exit
- `-c`, `--config`
  Path to the JSON configuration file (default: `~/.config/kanata/apps.json`)
- `-q`, `--quiet`
  Suppress non-essential output (only errors are shown)
- `-p`, `--port`
  kanata server port (e.g., `10000`) or full address (e.g., `127.0.0.1:10000`, default: `127.0.0.1:10000`)
- `-d`, `--debug`
  Enable debug mode
- `-v`, `--version`
  Show hyprkan version

> [!IMPORTANT]
> Ensure that the specified port or full address match those used by kanata to avoid connection issues.
