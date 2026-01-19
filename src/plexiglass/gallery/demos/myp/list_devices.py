"""
MyPlex Devices demo.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plexiglass.gallery.base_demo import BaseDemo

if TYPE_CHECKING:
    from plexapi.server import PlexServer


class MyPlexDevicesDemo(BaseDemo):
    """List devices on the MyPlex account."""

    name = "MyPlex Devices"
    description = "List devices linked to the Plex account"
    category = "MyPlex Account"
    operation_type = "READ"

    def get_code_example(self, params: dict[str, Any] | None = None) -> str:
        return """# List account devices
account = server.myPlexAccount()
for device in account.devices():
    print(device.name, device.product)
"""

    def execute(self, server: PlexServer | None, params: dict[str, Any]) -> dict[str, Any]:
        if server is None:
            return {"error": "No server connection available"}

        account = server.myPlexAccount()
        devices = []
        for device in list(account.devices()):
            devices.append(
                {
                    "name": getattr(device, "name", "Unknown"),
                    "product": getattr(device, "product", None),
                    "platform": getattr(device, "platform", None),
                    "clientIdentifier": getattr(device, "clientIdentifier", None),
                }
            )

        return {"devices": devices}
