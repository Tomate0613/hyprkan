import pytest
from src.hyprkan import utils


def test_is_blank():
    assert utils.is_blank("")
    assert utils.is_blank("   ")
    assert not utils.is_blank("a")
    assert not utils.is_blank("  b  ")


class TestValidatePort:

    @pytest.mark.parametrize(
        "valid_input,expected",
        [
            ("80", ("127.0.0.1", 80)),
            ("8080", ("127.0.0.1", 8080)),
            ("127.0.0.1:8000", ("127.0.0.1", 8000)),
            ("192.168.1.1:65535", ("192.168.1.1", 65535)),
        ],
    )
    def test_valid_ports(self, valid_input, expected):
        assert utils.validate_port(valid_input) == expected

    @pytest.mark.parametrize(
        "invalid_input",
        [
            "",
            "99999",
            "65536",
            "-1",
            "abcd",
            "127.0.0.1:99999",
            "127.0.0.1:-1",
            "256.0.0.1:80",
            "127.0.0.1",
            "1.1.1.1:",
            ":8080",
        ],
    )
    def test_invalid_ports(self, invalid_input, caplog):
        with caplog.at_level("ERROR"), pytest.raises(SystemExit):
            utils.validate_port(invalid_input)
            assert "Invalid value" in caplog.text


class TestRunCommand:

    def test_run_cmd(self):
        utils._run_cmd("whoami")

    def test_run_cmd_failure(self, caplog):
        with caplog.at_level("ERROR"), pytest.raises(SystemExit):
            utils._run_cmd("nonexistent_command_xyz")
            assert "Error occurred while running command" in caplog.text


class TestRequireEnv:

    def test_require_env_exists(self, monkeypatch):
        monkeypatch.setenv("TEST_VAR", "value")
        assert utils.require_env("TEST_VAR") == "value"

    def test_require_env_missing(self, monkeypatch):
        monkeypatch.delenv("TEST_VAR", raising=False)
        with pytest.raises(SystemExit):
            utils.require_env("TEST_VAR")


class TestValidateFakeKey:

    @pytest.mark.parametrize(
        "fake_key,rule_no,expected_message",
        [
            (("", "press"), None, "Fake key name must not be blank"),
            (("Jump", "hold"), None, "Invalid action 'Hold'. Must be one of"),
            (("Shoot", "smash"), 3, "Invalid config: rule #3 'Smash' must be one of"),
        ],
    )
    def test_invalid_fake_key_logs_and_exits(
        self, fake_key, rule_no, expected_message, caplog
    ):
        with caplog.at_level("ERROR"), pytest.raises(SystemExit):
            utils.validate_fake_key(fake_key, rule_no)

        assert expected_message in caplog.text
