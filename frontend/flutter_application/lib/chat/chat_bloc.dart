import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:http/http.dart' as http;
import 'dart:async';
import 'dart:convert';
import 'message.dart';

const String url = 'http://192.168.8.134:8080/api/chat';

class ChatState {
  final List<Message> messages;
  final bool isLoading;
  final String? error;

  ChatState({
    required this.messages,
    this.isLoading = false,
    this.error,
  });

  ChatState copyWith({
    List<Message>? messages,
    bool? isLoading,
    String? error,
  }) {
    return ChatState(
      messages: messages ?? this.messages,
      isLoading: isLoading ?? this.isLoading,
      error: error,
    );
  }
}

class ChatBloc extends Cubit<ChatState> {
  ChatBloc() : super(ChatState(messages: [])) {
    _startMessageChecking();
  }

  final TextEditingController messageController = TextEditingController();
  Timer? _messageCheckTimer;
  
  // TODO: These should come from login/settings
  String currentUser = 'a';
  String targetUser = 'b';

  void _startMessageChecking() {
    // Check for new messages every second
    _messageCheckTimer = Timer.periodic(
      const Duration(seconds: 1),
      (_) => checkForMessages(),
    );
  }

  @override
  Future<void> close() {
    _messageCheckTimer?.cancel();
    messageController.dispose();
    return super.close();
  }

  Future<void> sendMessage() async {
    final message = messageController.text.trim();
    if (message.isEmpty) return;

    // Add message to local state immediately
    final newMessage = Message(
      content: message,
      isUser: true,
      timestamp: DateTime.now(),
    );

    emit(state.copyWith(
      messages: [...state.messages, newMessage],
      isLoading: true,
      error: null,
    ));

    messageController.clear();

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'sendAddress': targetUser,
          'message': message,
        }),
      );

      if (response.statusCode != 200) {
        throw Exception('Failed to send message');
      }

      emit(state.copyWith(isLoading: false));
    } catch (e) {
      emit(state.copyWith(
        isLoading: false,
        error: 'Failed to send message: $e',
      ));
    }
  }

  Future<void> checkForMessages() async {
    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': currentUser,
        }),
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(response.body);
        final String? message = data['message'];
        
        if (message != null && message != 'No new messages') {
          final newMessage = Message(
            content: message,
            isUser: false,
            timestamp: DateTime.now(),
          );
          
          emit(state.copyWith(
            messages: [...state.messages, newMessage],
            error: null,
          ));
        }
      }
    } catch (e) {
      // Silent failure for periodic checks
      print('Error checking messages: $e');
    }
  }

  // Method to switch the current user (for testing)
  void switchUser() {
    final temp = currentUser;
    currentUser = targetUser;
    targetUser = temp;
    emit(state.copyWith(messages: [])); // Clear messages when switching users
  }
}