"""Text-to-Speech service using Hugging Face Transformers for Tagalog."""
from transformers import VitsModel, AutoTokenizer
import torch
import io
import scipy.io.wavfile


class TTSService:
    """Text-to-Speech service using facebook/mms-tts-tgl model."""
    
    def __init__(self):
        """Initialize the TTS model and tokenizer."""
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load the Hugging Face TTS model and tokenizer."""
        if self.model is None:
            self.model = VitsModel.from_pretrained("facebook/mms-tts-tgl")
            self.tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-tgl")
    
    def synthesize_speech(self, text: str, language: str = "tl-PH") -> bytes:
        """
        Synthesize speech from text using the Tagalog TTS model.
        
        Args:
            text: Text to convert to speech
            language: Language code (default: tl-PH for Tagalog)
        
        Returns:
            Audio bytes in WAV format
        """
        # Ensure model is loaded
        self._load_model()
        
        # Tokenize the text
        inputs = self.tokenizer(text, return_tensors="pt")
        
        # Generate speech waveform
        with torch.no_grad():
            output = self.model(**inputs).waveform
        
        # Convert tensor to numpy array
        waveform = output.squeeze().cpu().numpy()
        
        # Create in-memory bytes buffer
        audio_buffer = io.BytesIO()
        scipy.io.wavfile.write(
            audio_buffer,
            rate=self.model.config.sampling_rate,
            data=waveform
        )
        
        # Get the bytes and return
        audio_buffer.seek(0)
        return audio_buffer.read()


# Create singleton instance
tts_service = TTSService()


