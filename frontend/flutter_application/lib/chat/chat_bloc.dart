import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter/material.dart';
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

class ChatBloc extends Cubit<ChatState> {
  final TextEditingController messageController = TextEditingController();

  ChatBloc() : super(ChatState(messages: []));

  void sendMessage() async {
    if (messageController.text.trim().isEmpty) return;

    final newMessage = Message(
      content: messageController.text,
      isUser: true,
      timestamp: DateTime.now(),
    );

    // Add user message to the chat
    emit(state.copyWith(
      messages: [...state.messages, newMessage],
      isLoading: true,
    ));

    // Clear the input field
    messageController.clear();

    try {
      // Call your API here
      // final response = await yourApiCall(newMessage.content);
      
      // Simulate API response for now
      await Future.delayed(const Duration(seconds: 1));
      final botResponse = Message(
        content: "This is a bot response",
        isUser: false,
        timestamp: DateTime.now(),
      );

      // Add bot response to the chat
      emit(state.copyWith(
        messages: [...state.messages, botResponse],
        isLoading: false,
      ));
    } catch (e) {
      emit(state.copyWith(isLoading: false));
      // Handle error
    }
  }
}