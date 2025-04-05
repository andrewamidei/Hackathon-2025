import 'package:flutter/material.dart';  // Add this import
import 'package:flutter_bloc/flutter_bloc.dart';
import 'message.dart';
import 'dart:async';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'chat_state.dart';

class ChatBloc extends Cubit<ChatState> {
  final TextEditingController messageController = TextEditingController();
  final String currentUser;
  final String receiver;
  Timer? _pollTimer;

  ChatBloc({
    required this.currentUser,
    required this.receiver,
  }) : super(ChatState(messages: [])) {
    // Start polling for new messages
    _pollTimer = Timer.periodic(
      const Duration(seconds: 2),
      (_) => _pollMessages(),
    );
  }

  void sendMessage() async {
    if (messageController.text.trim().isEmpty) return;

    final newMessage = Message(
      content: messageController.text,
      sender: currentUser,
      receiver: receiver,
      isUser: true,
      timestamp: DateTime.now(),
    );

    emit(state.copyWith(
      messages: [...state.messages, newMessage],
      isLoading: true,
    ));

    messageController.clear();

    try {
      final response = await http.post(
        Uri.parse('http://localhost:8080/api/chat/send'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'sender': currentUser,
          'receiver': receiver,
          'content': newMessage.content,
        }),
      );

      if (response.statusCode != 200) {
        throw Exception('Failed to send message');
      }
    } catch (e) {
      emit(state.copyWith(isLoading: false));
    }
  }

  Future<void> _pollMessages() async {
    try {
      final response = await http.get(
        Uri.parse('http://localhost:8080/api/chat/receive/$currentUser'),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final newMessages = (data['messages'] as List).map((m) => Message(
          content: m['content'],
          sender: m['sender'],
          receiver: currentUser,
          isUser: m['sender'] == currentUser,
          timestamp: DateTime.parse(m['timestamp']),
        )).toList();

        if (newMessages.isNotEmpty) {
          emit(state.copyWith(
            messages: [...state.messages, ...newMessages],
            isLoading: false,
          ));
        }
      }
    } catch (e) {
      print('Error polling messages: $e');
    }
  }

  @override
  Future<void> close() {
    _pollTimer?.cancel();
    return super.close();
  }
}