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
            logging.debug(f"Added raw message from {message.sender} to {message.receiver}: {message.content}")

    def get_next_raw_message(self) -> ChatMessage | None:
        """Get and remove the next raw message from the queue"""
        with self._lock:
            if not self._raw_messages:
                return None
            message = self._raw_messages.popleft()
            logging.debug(f"Retrieved raw message from {message.sender}")
            return message

    def get_processed_messages(self, username: str) -> list[ChatMessage]:
        with self._lock:
            if username not in self._processed_messages:
                return []
            messages = list(self._processed_messages[username])
            if messages:  # Only clear if there are messages
                self._processed_messages[username].clear()
                logging.debug(f"Retrieved and cleared {len(messages)} messages for {username}")
            return messages
    
    def add_processed_message(self, message: ChatMessage):
        with self._lock:
            if message.receiver not in self._processed_messages:
                self._processed_messages[message.receiver] = deque()
            self._processed_messages[message.receiver].append(message)
            logging.debug(f"Added processed message for {message.receiver}: {message.content}")