import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:http/http.dart' as http;
import 'dart:async';
import 'dart:convert';
import 'message.dart';

const String url = 'http://192.168.8.134:8080/api/chat';
const String dockerurl = 'http://192.168.8.137:8080/api/queryllm';

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
      // Format message using LLM before sending
      final formattedMessage = await sendMessageToLLM(message);
      final messageToSend = formattedMessage ?? message; // Use original if formatting fails

      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'sendAddress': targetUser,
          'message': messageToSend,
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

  Future<String?> sendMessageToLLM(String message) async {
    String discOne = "Happy";
    String discTwo = "Joyful"; 

    String prompt = """
                    You are an AI that transforms customer messages for internal use.

                    Your job is to take the original message below and rewrite it in a way that is more $discOne and $discTwo — while keeping the original meaning of the message the same.

                    ⚠️ DO NOT respond to the message. DO NOT comment on it. DO NOT change the meaning.

                    Only rephrase the message in a new tone and return the modified version **only**.

                    Original Message:
                    "$message"

                  Output:
                  <transformed message only – no explanation, no intro, no formatting>
                  """;

    String rating = """You are a classifier.

                    Respond only with a single integer between 0 and 10 representing the aggressiveness of the following message.

                    DO NOT explain, do not label, do not output anything else. Only give the number.

                    Message:  "$message" """;

    try {
      final response = await http.post(
        Uri.parse(dockerurl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'prompt': prompt, 'ratePrompt': rating})
      );

      if (response.statusCode == 200) {
        Map<String, dynamic> map = jsonDecode(response.body);
        return map["response"];
      } else {
        print('Failed to format message: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('Failed to connect to the LLM server: $e');
      return null;
    }
  }
}