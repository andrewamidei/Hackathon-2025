class Message {
  final String content;
  final String sender;
  final String receiver;
  final bool isUser;
  final DateTime timestamp;

  Message({
    required this.content,
    required this.sender,
    required this.receiver,
    required this.isUser,
    required this.timestamp,
  });
}