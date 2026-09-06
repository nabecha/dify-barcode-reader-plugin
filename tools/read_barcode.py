import io
from collections.abc import Generator
from typing import Any

import numpy as np
import zxingcpp
from PIL import Image, UnidentifiedImageError

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.file.file import File


class ReadBarcodeTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        image = tool_parameters.get("image")

        if not isinstance(image, File):
            yield self.create_text_message("A valid image file is required.")
            return

        try:
            image_bytes = image.blob

            with Image.open(io.BytesIO(image_bytes)) as pil_image:
                # Normalize EXIF rotation and color mode for stable decoding.
                pil_image = pil_image.convert("RGB")
                image_array = np.asarray(pil_image)

            results = zxingcpp.read_barcodes(image_array)

        except UnidentifiedImageError:
            yield self.create_text_message(
                "The uploaded file could not be opened as an image."
            )
            return
        except Exception as exc:
            yield self.create_text_message(
                f"Barcode decoding failed: {type(exc).__name__}: {exc}"
            )
            return

        if not results:
            yield self.create_variable_message("found", False)
            yield self.create_variable_message("barcode", "")
            yield self.create_variable_message("format", "")
            yield self.create_variable_message("count", 0)
            yield self.create_variable_message("all_barcodes", [])
            yield self.create_json_message(
                {
                    "found": False,
                    "barcode": "",
                    "format": "",
                    "count": 0,
                    "all_barcodes": [],
                }
            )
            yield self.create_text_message(
                "No barcode was detected in the uploaded image."
            )
            return

        values = [result.text for result in results]
        first = results[0]
        barcode_format = str(first.format)

        yield self.create_variable_message("found", True)
        yield self.create_variable_message("barcode", first.text)
        yield self.create_variable_message("format", barcode_format)
        yield self.create_variable_message("count", len(results))
        yield self.create_variable_message("all_barcodes", values)

        yield self.create_json_message(
            {
                "found": True,
                "barcode": first.text,
                "format": barcode_format,
                "count": len(results),
                "all_barcodes": values,
            }
        )

        yield self.create_text_message(
            f"Barcode: {first.text}\nFormat: {barcode_format}"
        )
