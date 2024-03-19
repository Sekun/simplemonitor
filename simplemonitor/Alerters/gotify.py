"""
SimpleMonitor alerts via Gotify
"""

from typing import cast
from urllib.parse import urljoin

import requests

from ..Monitors.monitor import Monitor
from .alerter import Alerter, AlertLength, AlertType, register


@register
class GotifyAlerter(Alerter):
    """Send push notification via Gotify."""

    alerter_type = "gotify"

    def __init__(self, config_options: dict) -> None:
        super().__init__(config_options)

        self.gotify_url = cast(
            str, self.get_config_option("url", required=True, allow_empty=False)
        )

        self.gotify_token = cast(
            str, self.get_config_option("token", required=True, allow_empty=False)
        )

        self.timeout = cast(
            int, self.get_config_option("timeout", required_type="int", default=5)
        )

        self.support_catchup = True

    def send_gotify_notification(self, subject: str, body: str) -> None:
        """Send a push notification."""

        gotify_msg_url = urljoin(self.gotify_url, "/message")
        response = requests.post(
            gotify_msg_url,
            params={"token": self.gotify_token},
            data={"title": subject, "message": body},
            timeout=self.timeout,
        )
        if not response.status_code == requests.codes.ok:
            raise RuntimeError("Unable to send gotify notification")

    def send_alert(self, name: str, monitor: Monitor) -> None:
        """Build up the content for the push notification."""

        alert_type = self.should_alert(monitor)
        if alert_type == AlertType.NONE:
            return

        subject = self.build_message(AlertLength.NOTIFICATION, alert_type, monitor)
        body = self.build_message(AlertLength.FULL, alert_type, monitor)

        if not self._dry_run:
            try:
                self.send_gotify_notification(subject, body)
            except Exception:
                self.alerter_logger.exception("Couldn't send push notification")
        else:
            self.alerter_logger.info("dry_run: would send push notification: %s", body)

    def _describe_action(self) -> str:
        return "posting messages to Gotify"
