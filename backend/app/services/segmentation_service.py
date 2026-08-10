from app.core.segmentation import segment_text, SegmentationResult
from app.services.dictionary_service import DictionaryService

class SegmentationService:
    def __init__(self, dictionary_service: DictionaryService):
        self.dictionary_service = dictionary_service

    def segment(self, text: str) -> SegmentationResult | None:
        if not text:
            return None

        word_freq = {word: entry.frequency for word, entry in self.dictionary_service.entries.items()}

        total_freq = self.dictionary_service.total_frequency
        if total_freq <= 0:
            return None

        return segment_text(text, word_freq, total_freq)