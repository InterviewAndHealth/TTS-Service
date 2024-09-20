import wave
import io


class BrowserHandler:
    """Helper class to handle browser-specific requests."""

    BROWSER_IDENTIFIERS = [
        "mozilla",
        "chrome",
        "safari",
        "firefox",
        "edge",
        "opera",
        "msie",
        "trident",
    ]

    @staticmethod
    def is_browser_request(request):
        """Check if the request is from a browser."""
        user_agent = request.headers.get("user-agent", "").lower()
        is_browser = any(
            browser_id in user_agent
            for browser_id in BrowserHandler.BROWSER_IDENTIFIERS
        )
        return is_browser

    @staticmethod
    def create_wave_header_for_engine(engine):
        """Create a wave header for the given engine."""
        _, _, sample_rate = engine.get_stream_info()

        num_channels = 1
        sample_width = 2
        frame_rate = sample_rate

        wav_header = io.BytesIO()
        with wave.open(wav_header, "wb") as wav_file:
            wav_file.setnchannels(num_channels)
            wav_file.setsampwidth(sample_width)
            wav_file.setframerate(frame_rate)

        wav_header.seek(0)
        wave_header_bytes = wav_header.read()
        wav_header.close()

        # Create a new BytesIO with the correct MIME type for Firefox
        final_wave_header = io.BytesIO()
        final_wave_header.write(wave_header_bytes)
        final_wave_header.seek(0)

        return final_wave_header.getvalue()
