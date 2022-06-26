from abc import ABC, abstractmethod



class QuoteStream(ABC):
    
    @abstractmethod
    def handle_messages(self):
        raise NotImplementedError('handle_messages is not implemented yet')

    @abstractmethod
    def start_stream(self):
        raise NotImplementedError('start_stream is not implemented yet')

