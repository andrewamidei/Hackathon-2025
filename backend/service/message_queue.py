from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Deque
import threading
import logging

@dataclass
class ChatMessage:
    sender: str
    receiver: str
    content: str
    timestamp: datetime
    processed: bool = False

class MessageQueue:
    def __init__(self):
        self._raw_messages: Deque[ChatMessage] = deque()
        self._processed_messages: Dict[str, Deque[ChatMessage]] = {}
        self._lock = threading.Lock()
        
    def add_raw_message(self, message: ChatMessage):
        with self._lock:
            self._raw_messages.append(message)
            logging.debug(f"Added raw message: {message}")
    
    def get_next_raw_message(self) -> ChatMessage | None:
        with self._lock:
            return self._raw_messages.popleft() if self._raw_messages else None
    
    def add_processed_message(self, message: ChatMessage):
        with self._lock:
            if message.receiver not in self._processed_messages:
                self._processed_messages[message.receiver] = deque()
            self._processed_messages[message.receiver].append(message)
            logging.debug(f"Added processed message for {message.receiver}: {message}")
    
    def get_processed_messages(self, username: str) -> list[ChatMessage]:
        with self._lock:
            if username not in self._processed_messages:
                return []
            messages = list(self._processed_messages[username])
            self._processed_messages[username].clear()
            return messages