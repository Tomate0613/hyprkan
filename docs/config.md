## Hyprkan Configuration

Hyprkan configuration is a [JSON](https://en.wikipedia.org/wiki/JSON) file where you define window rules and the corresponding kanata layers.

**Default path:**

`$XDG_CONFIG_HOME/kanata/apps.json`
You can override this using the `-c` or `--config <path>` option.

**Example configuration file:**

```json
[
  {
    "class": "Inkscape",
    "title": "New document",
    "fake_key": ["esc", "tap"],
    "layer": "inkscape-layer"
  },
  { "class": "*", "title": "ChatGPT", "layer": "ai_layer" },
  { "class": false, "title": "VLC media player", "layer": null },
  { "class": "*", "title": "*", "layer": "base_layer" }
]
```

## Defining Rules

The config is a list of rules. Each rule can include:

- `"class"` Window class
- `"title"` Window title
- `"layer"`: Kanata layer to change to
- `"cmd"`: Shell command to execute
- `"fake_key"`: Kanata virtual key to trigger (e.g. `["esc", "tap"]`)
- `"set_mouse"`: Mouse position to set (e.g. `[300, 400]`)

## Adding a New Rule

Let’s say you want to automatically switch to a specific Kanata layer when the focused window’s class is `"kitty"` and its title is `"vim"`.

<!-- prettier-ignore -->
```jsonc
{
  "class": "^kitty$",     // exact match for window class "kitty"
  "title": "^vim$",       // exact match for window title "vim"
  "layer": "vim_layer",   // change to this Kanata layer
}
```

> [!NOTE]
> Use `--current-window-info [seconds]` to print the current window's class and title.

## Matching Behavior

Each rule matches a window based on its class and title.

- `"class"` and `"title"` use **regular expressions**

```jsonc
{ "class": "term" } // matches "foot-terminal", "coolterm", etc.
```

- If no anchors (`^`, `$`) are used, the value matches **anywhere inside** the class or title

```jsonc
{ "title": "vim" } // matches "vim - main.c", "neovim", etc.
```

- Use anchors to match exact names

```jsonc
{ "class": "^kitty$", "title": "^vim$" } // matches only if class is exactly "kitty" and title is exactly "vim"
```

- The wildcard `"*"` matches **any class** or **any title**

```jsonc
{ "class": "*", "title": "ChatGPT" } // matches any app with title containing "ChatGPT"
```

- If both `"class"` and `"title"` are provided, **both must match**

```jsonc
{ "class": "^code$", "title": "^main.c$" } // matches a window from "code" titled exactly "main.c"
```

- If **neither** is specified, the rule matches **any window**

```jsonc
{ "layer": "default" } // fallback if no class or title match
```

- If `"layer"` is set to `null` or `false`, the rule disables switching for matching windows

```jsonc
{ "class": "vlc", "layer": null } // ignore this window
```

- Matching is done **top to bottom**—the first matching rule is used
- Add a catch-all fallback rule at the end using `"*"` for both class and title

```jsonc
{
  "class": "*",
  "title": "*",
  "layer": "base_layer" // default layer for unmatched windows
}

// Or simply:

{ "layer": "base_layer" }
```

> [!IMPORTANT]
> If the previous rule is placed at the top, it will always match first, and no other rules below it will be checked.
> Always place it **last** to ensure it's only used when no other rule matches.
