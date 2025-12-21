import asyncio
import importlib.util
from concurrent import futures

from . import _base

# Attempt to find winsdk module and let error propagate if it is not available. We don't want to
# import winsdk here because it needs to be done in a background thread.
if not importlib.util.find_spec("winsdk"):
    raise ImportError("Could not find winsdk module")


class WinRtBackend(_base.OcrBackend):
    def __init__(self, language_tag: str = None):
        # Run all winsdk interactions on a new thread to avoid
        # "RuntimeError: Cannot change thread mode after it is set."
        # from import winsdk.
        self._executor = futures.ThreadPoolExecutor(max_workers=1)
        self._executor.submit(self._init_winrt, language_tag).result()

    def _init_winrt(self, language_tag):
        import winsdk  # noqa: F401
        import winsdk.windows.graphics.imaging as imaging
        import winsdk.windows.media.ocr as ocr
        import winsdk.windows.storage.streams as streams

        engine = None
        if language_tag is None:
            engine = ocr.OcrEngine.try_create_from_user_profile_languages()
        else:
            for language in ocr.OcrEngine.get_available_recognizer_languages():
                if language.language_tag == language_tag:
                    engine = ocr.OcrEngine.try_create_from_language(language)
                    break

        if not engine:
            raise RuntimeError(
                "Could not create OcrEngine. Try installing language packs: "
                "https://github.com/wolfmanstout/screen-ocr/issues/8#issuecomment-1219610003"
            )

        # Define this in the constructor to avoid SyntaxError in Python 2.7.
        async def run_ocr_async(image):
            bytes = image.convert("RGBA").tobytes()
            data_writer = streams.DataWriter()
            data_writer.write_bytes(bytes)
            del bytes
            bitmap = imaging.SoftwareBitmap(
                imaging.BitmapPixelFormat.RGBA8, image.width, image.height
            )
            bitmap.copy_from_buffer(data_writer.detach_buffer())
            del data_writer
            result = await engine.recognize_async(bitmap)
            lines = [
                _base.OcrLine(
                    [
                        _base.OcrWord(
                            word.text,
                            word.bounding_rect.x,
                            word.bounding_rect.y,
                            word.bounding_rect.width,
                            word.bounding_rect.height,
                        )
                        for word in line.words
                    ]
                )
                for line in result.lines
            ]
            return _base.OcrResult(lines)

        self._run_ocr_async = run_ocr_async

    def run_ocr(self, image):
        return self._executor.submit(
            lambda: asyncio.run(self._run_ocr_async(image))
        ).result()
