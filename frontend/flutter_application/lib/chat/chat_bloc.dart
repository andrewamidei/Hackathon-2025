import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:http/http.dart' as http;
import 'dart:async';
import 'dart:convert';
import 'message.dart';

const String chatUrl = 'http://192.168.8.137:8080/api/chat';
const String llmUrl = 'http://192.168.8.137:8080/api/queryllm';

class ChatState {
  final List<Message> messages;
  final bool isLoading;
  final String? error;
  final bool botMode;

  ChatState({
    required this.messages,
    this.isLoading = false,
    this.error,
    this.botMode = false,
  });

  ChatState copyWith({
    List<Message>? messages,
    bool? isLoading,
    String? error,
    bool? botMode,
  }) {
    return ChatState(
      messages: messages ?? this.messages,
      isLoading: isLoading ?? this.isLoading,
      error: error,
      botMode: botMode ?? this.botMode,
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
  String currentUser = 'b';
  String targetUser = 'a';

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
      // First process through LLM if needed
      final llmResult = await sendMessageToLLM(message);
      
      if (llmResult == null) {
        throw Exception('Failed to process message');
      }

      final int score = llmResult['score'] as int;
      String messageToSend;

      if (score >= 8) {
        // High aggression - close chat and switch to AI mode
        messageToSend = "Chat has been closed due to aggressive content. Switching to AI chat mode.";
      } else if (score >= 5) {
        // Medium aggression - use LLM formatted message
        messageToSend = llmResult['response'] as String;
      } else {
        // Low aggression - use original message
        messageToSend = message;
      }

      // Send message to chat server
      final response = await http.post(
        Uri.parse(chatUrl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'sendAddress': targetUser,
          'message': messageToSend,
        }),
      );

      if (response.statusCode == 200) {
        final responseData = jsonDecode(response.body);
        if (responseData['status'] == 'Message sent successfully') {
          // If this was a high aggression message, switch to AI mode after confirming send
          if (score >= 8) {
            await switchToLLM(true);
          }
          emit(state.copyWith(isLoading: false));
        } else {
          throw Exception('Failed to send message: ${responseData['error'] ?? 'Unknown error'}');
        }
      } else {
        throw Exception('Failed to send message: Server returned ${response.statusCode}');
      }
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
        Uri.parse(chatUrl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': currentUser,
        }),
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(response.body);
        final String? message = data['message'];
        final bool? newBotMode = data['botMode'];
        
        // Update bot mode if it changed
        if (newBotMode != null && newBotMode != state.botMode) {
          await switchToLLM(newBotMode);
        }
        
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

  Future<Map<String, dynamic>?> sendMessageToLLM(String message) async {
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
        Uri.parse(llmUrl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'prompt': prompt, 'rate_prompt': rating})
      );

      if (response.statusCode == 200) {
        Map<String, dynamic> map = jsonDecode(response.body);
        final scoreStr = map["score"]?.toString() ?? "0";
        final score = int.tryParse(scoreStr) ?? 0;
        
        return {
          'response': map["response"] as String? ?? message,
          'score': score
        };
      } else {
        print('Failed to format message: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('Failed to connect to the LLM server: $e');
      return null;
    }
  }

  Future<void> switchToLLM(bool isActive) async {
    if (isActive == state.botMode) return; // No change needed

    emit(state.copyWith(
      botMode: isActive,
      messages: [], // Clear messages when switching modes
      error: null,
    ));

    if (isActive) {
      // Stop periodic message checking when in AI mode
      _messageCheckTimer?.cancel();
      _messageCheckTimer = null;
      
      // Add welcome message for AI chat mode
      final welcomeMessage = Message(
        content: "You are now chatting with an AI assistant. How can I help you today?",
        isUser: false,
        timestamp: DateTime.now(),
      );
      
      emit(state.copyWith(
        messages: [...state.messages, welcomeMessage],
      ));
    } else {
      // Restart periodic message checking when returning to normal chat
      _startMessageChecking();
    }
  }
}