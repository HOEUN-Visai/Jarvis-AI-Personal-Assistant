import threading
import logging
import pyttsx3
import queue

from jarvis.core.console import ConsoleManager

class TTSEngine:
    def __init__(self):
        self.tts_engine = self._set_voice_engine()
        self.logger = logging.getLogger(__name__)
        self.message_queue = queue.Queue(maxsize=100)  # Adjust based on expected workload
        self.stop_speaking = False
        self.console_manager = ConsoleManager()
        self.volume = 1.0  # Default volume level
        self.rate = 100  # Default speech rate (100 words per minute)

    def assistant_response(self, message, refresh_console=True):
        self._insert_into_message_queue(message)
        try:
            speech_thread = threading.Thread(target=self._speech_and_console, args=(refresh_console,))
            speech_thread.start()
        except RuntimeError as e:
            self.logger.error(f"Error in assistant response thread: {e}")

    def _insert_into_message_queue(self, message):
        try:
            self.message_queue.put(message)
        except Exception as e:
            self.logger.error(f"Unable to insert message into queue: {e}")

    def _speech_and_console(self, refresh_console):
        try:
            while not self.message_queue.empty():
                cumulative_batch = ''
                message = self.message_queue.get()
                if message:
                    batches = self._create_text_batches(raw_text=message)
                    for batch in batches:
                        self.tts_engine.say(batch)
                        cumulative_batch += batch
                        self.console_manager.console_output(cumulative_batch, refresh_console=refresh_console)
                        self.run_engine()
                        if self.stop_speaking:
                            self.logger.debug('Speech interruption triggered')
                            self.stop_speaking = False
                            break
        except Exception as e:
            self.logger.error(f"Speech and console error: {e}")

    def _create_text_batches(self, raw_text, number_of_words_per_batch=8):
        raw_text += ' '
        list_of_batches = []
        total_words = raw_text.count(' ')
        letter_id = 0

        for _ in range(0, total_words // number_of_words_per_batch):
            batch = ''
            words_count = 0
            while words_count < number_of_words_per_batch:
                batch += raw_text[letter_id]
                if raw_text[letter_id] == ' ':
                    words_count += 1
                letter_id += 1
            list_of_batches.append(batch)

        if letter_id < len(raw_text):
            list_of_batches.append(raw_text[letter_id:])
        return list_of_batches

    def run_engine(self):
        try:
            self.tts_engine.runAndWait()
        except RuntimeError as e:
            self.logger.error(f"Error in TTS engine: {e}")

    def set_volume(self, volume):
        """
        Set the volume level of the TTS engine.
        :param volume: float between 0.0 and 1.0
        """
        if 0.0 <= volume <= 1.0:
            self.volume = volume
            self.tts_engine.setProperty('volume', volume)
        else:
            self.logger.warning("Volume level should be between 0.0 and 1.0")

    def set_rate(self, rate):
        """
        Set the speech rate of the TTS engine.
        :param rate: int speech rate in words per minute (WPM)
        """
        if rate > 0:
            self.rate = rate
            self.tts_engine.setProperty('rate', rate)
        else:
            self.logger.warning("Speech rate should be greater than 0")

    @staticmethod
    def _set_voice_engine():
        tts_engine = pyttsx3.init()
        tts_engine.setProperty('rate', 150)  # Set default speech rate to 150 WPM
        return tts_engine
