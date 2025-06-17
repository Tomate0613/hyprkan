# Setting Up Hyprkan as a Service

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

> [!IMPORTANT]
> Make sure to replace `%h/.local/bin/hyprkan` with the correct path to the hyprkan script.

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
