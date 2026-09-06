from typing import Any

from dify_plugin import ToolProvider


class BarcodeReaderProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # This plugin does not require credentials.
        return None
