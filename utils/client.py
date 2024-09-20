from fastapi.responses import StreamingResponse
from RealtimeTTS import TextToAudioStream
from queue import Queue
import threading
import logging


from .engine import Engine
from .browser import BrowserHandler

play_text_to_speech_semaphore = threading.Semaphore(1)
tts_lock = threading.Lock()


class ClientConnection:
    """Handle a client connection for text-to-speech streaming."""

    def __init__(self):
        self.engine = Engine.get_instance()
        self.audio_queue = Queue()
        self.stream = TextToAudioStream(
            self.engine, on_audio_stream_stop=self.on_audio_stream_stop, muted=True
        )
        self.speaking = False

    def handle(self, request, text):
        """Handle request"""
        with tts_lock:
            browser_request = BrowserHandler.is_browser_request(request)

            if play_text_to_speech_semaphore.acquire(blocking=False):
                try:
                    threading.Thread(
                        target=self.play_text_to_speech,
                        args=(text,),
                        daemon=True,
                    ).start()
                finally:
                    play_text_to_speech_semaphore.release()

            return StreamingResponse(
                self.audio_chunk_generator(browser_request),
                media_type="audio/wav",
            )

    def on_audio_chunk(self, chunk):
        self.audio_queue.put(chunk)

    def on_audio_stream_stop(self):
        self.audio_queue.put(None)
        self.speaking = False

    def play_text_to_speech(self, text):
        self.speaking = True
        self.stream.feed(text)
        logging.debug(f"Playing audio for text: {text}")
        self.stream.play_async(on_audio_chunk=self.on_audio_chunk, muted=True)

    def audio_chunk_generator(self, send_wave_headers):
        first_chunk = False
        try:
            while True:
                chunk = self.audio_queue.get()
                if chunk is None:
                    logging.debug("End of audio stream")
                    break
                if not first_chunk:
                    if send_wave_headers:
                        logging.debug("Sending wave header")
                        yield BrowserHandler.create_wave_header_for_engine(self.engine)
                    first_chunk = True
                yield chunk
        except Exception as e:
            logging.error(f"Error during streaming: {str(e)}")
