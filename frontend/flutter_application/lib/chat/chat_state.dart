import 'message.dart';

class ChatState {
  final List<Message> messages;
  final bool isLoading;

  ChatState({
    required this.messages,
    this.isLoading = false,
  });

  ChatState copyWith({
    List<Message>? messages,
    bool? isLoading,
  }) {
    return ChatState(
      messages: messages ?? this.messages,
      isLoading: isLoading ?? this.isLoading,
    );
  }
}