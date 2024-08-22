import re

import pytest

from pretiac.client import Client
from pretiac.exceptions import PretiacRequestException


class TestList:
    def test_hosts(self, client: Client) -> None:
        results = client.objects.list("Host")
        host = results[0]
        assert host["attrs"]["address"] == "127.0.0.1"
        assert set(host["attrs"].keys()) == set(
            [
                "__name",
                "acknowledgement",
                "acknowledgement_expiry",
                "acknowledgement_last_change",
                "action_url",
                "active",
                "address",
                "address6",
                "check_attempt",
                "check_command",
                "check_interval",
                "check_period",
                "check_timeout",
                "command_endpoint",
                "display_name",
                "downtime_depth",
                "enable_active_checks",
                "enable_event_handler",
                "enable_flapping",
                "enable_notifications",
                "enable_passive_checks",
                "enable_perfdata",
                "event_command",
                "executions",
                "flapping",
                "flapping_current",
                "flapping_ignore_states",
                "flapping_last_change",
                "flapping_threshold",
                "flapping_threshold_high",
                "flapping_threshold_low",
                "force_next_check",
                "force_next_notification",
                "groups",
                "ha_mode",
                "handled",
                "icon_image",
                "icon_image_alt",
                "last_check",
                "last_check_result",
                "last_hard_state",
                "last_hard_state_change",
                "last_reachable",
                "last_state",
                "last_state_change",
                "last_state_down",
                "last_state_type",
                "last_state_unreachable",
                "last_state_up",
                "max_check_attempts",
                "name",
                "next_check",
                "next_update",
                "notes",
                "notes_url",
                "original_attributes",
                "package",
                "paused",
                "previous_state_change",
                "problem",
                "retry_interval",
                "severity",
                "source_location",
                "state",
                "state_type",
                "templates",
                "type",
                "vars",
                "version",
                "volatile",
                "zone",
            ]
        )

    def test_attrs(self, client: Client) -> None:
        results = client.objects.list("Host", attrs=("address", "notes"))
        host = results[0]
        assert host["attrs"]["address"] == "127.0.0.1"
        assert set(host["attrs"].keys()) == set(
            [
                "address",
                "notes",
            ]
        )

    def test_exception(self, client: Client) -> None:
        with pytest.raises(PretiacRequestException, match="No objects found."):
            client.objects.list("Host", "XXX")

    def test_suppress_exception(self, client: Client) -> None:
        result = client.objects.list("Host", "XXX", suppress_exception=True)
        assert result["error"] == 404
        assert result["status"] == "No objects found."


class TestGet:
    def test_host(self, client: Client) -> None:
        host = client.objects.get("Host", "Host1")
        assert host["attrs"]["name"] == "Host1"
        assert host["attrs"]["address"] == "127.0.0.1"


class TestCreate:
    def test_create(self, client: Client) -> None:
        client.objects.delete("Service", "Host1!custom-load", suppress_exception=True)
        result = client.objects.create(
            "Service",
            "Host1!custom-load",
            templates=["generic-service"],
            attrs={"check_command": "load", "check_interval": 1, "retry_interval": 1},
        )
        assert result["results"][0]["code"] == 200
        assert result["results"][0]["status"] == "Object was created"

    def test_create_minimal(self, client: Client) -> None:
        """Create with minimal arguments"""
        client.objects.delete("Service", "Host1!custom-load", suppress_exception=True)
        result = client.objects.create(
            "Service",
            "Host1!custom-load",
            attrs={"check_command": "load"},
        )
        assert result["results"][0]["code"] == 200
        assert result["results"][0]["status"] == "Object was created"

    def test_error(self, client: Client) -> None:
        result = client.objects.create(
            "Service",
            "Host1!xxx",
            suppress_exception=True,
        )
        error = result["results"][0]
        assert error["code"] == 500
        assert re.match(
            r"Error: Validation failed for object 'Host1!xxx' of type 'Service'; Attribute 'check_command': Attribute must not be empty.\nLocation: in /var/lib/icinga2/api/packages/_api/.*/conf.d/services/Host1!xxx.conf:",
            error["errors"][0],
        )
        assert error["status"] == "Object could not be created."
