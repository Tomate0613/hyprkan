import json
import tempfile
from pathlib import Path
import pytest
from src.hyprkan import Config, Kanata

VALID_CONFIG_PATH = Path(__file__).parent / "fixtures" / "valid_config.json"
INVALID_CONFIG_PATH = Path(__file__).parent / "fixtures" / "invalid_configs.json"
KANATA_LAYERS = [
    "media",
    "dev",
    "chat",
    "docs",
    "base_layer",
    "shell",
    "ai_layer",
    "vs_code",
    "lang_html",
    "lang_css",
    "gaming",
    "streaming",
    "vim_scratch",
]


class DummyKanata(Kanata):
    def __init__(self, layers: list[str]):
        self._layers = layers

    def get_layer_names(self) -> list[str]:
        return self._layers


def write_temp_config(rules: list[dict]) -> str:
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".json", mode="w"
    ) as tmp_file:
        json.dump(rules, tmp_file)
        return tmp_file.name


def load_invalid_configs():
    path = INVALID_CONFIG_PATH
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_rules_from_fixture() -> list[dict]:
    path = VALID_CONFIG_PATH
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class TestConfigValidation:
    def test_valid_config_passes(self, caplog):
        rules = load_rules_from_fixture()
        path = write_temp_config(rules)
        with caplog.at_level("INFO"):
            config = Config(path, DummyKanata(KANATA_LAYERS))
        assert config.rules == rules
        assert "Configuration at" in caplog.text

    @pytest.mark.parametrize("rules, error_msg", load_invalid_configs())
    def test_invalid_configs_fail(self, rules, error_msg, caplog):
        path = write_temp_config(rules)
        with caplog.at_level("ERROR"), pytest.raises(SystemExit):
            Config(path, DummyKanata(KANATA_LAYERS))
        assert error_msg in caplog.text


class TestRuleMatching:
    @pytest.mark.parametrize(
        "win_info, expected_rule",
        [
            (
                {"cls": "chrome", "title": "YouTube"},
                {"class": "chrome", "title": "YouTube", "layer": "media"},
            ),
            (
                {"cls": "code-oss", "title": "index.html - Code - OSS"},
                {"class": "code-oss", "title": "*", "layer": "vs_code"},
            ),
            (
                {"cls": "vlc", "title": "Movie"},
                {
                    "class": "vlc",
                    "title": "Movie",
                    "layer": "media",
                    "fake_key": ["Space", "Tap"],
                    "set_mouse": [300, 400],
                },
            ),
            (
                {"cls": "nvim", "title": "nvim - [Scratch]"},
                {
                    "class": "nvim",
                    "title": "nvim - \\[Scratch]",
                    "layer": "vim_scratch",
                },
            ),
            (
                {"cls": "Steam", "title": "Library"},
                {"class": "Steam", "title": "Library", "layer": "gaming"},
            ),
            (
                {"cls": "obs", "title": "Recording"},
                {"class": "^obs$", "layer": "streaming"},
            ),
            (
                {"cls": "random", "title": "ChatGPT"},
                {"class": "*", "title": "ChatGPT", "layer": "ai_layer"},
            ),
            (
                {"cls": "any", "title": "README.md"},
                {"title": "README", "layer": "docs"},
            ),
            (
                {"cls": "something", "title": "unknown"},
                {"class": "*", "title": "*", "layer": "base_layer"},
            ),
        ],
    )
    def test_detect_rule_matches(self, win_info, expected_rule):
        valid_config_path = VALID_CONFIG_PATH
        config = Config(
            str(valid_config_path),
            DummyKanata(KANATA_LAYERS),
        )
        assert config.detect_rule(win_info) == expected_rule
