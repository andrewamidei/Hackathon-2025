import 'package:flutter/material.dart';
import 'chat/chat_page.dart';
import 'navigation/navigation_page.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: ChatPage(),
      //home: NavigationPage(),
    );
  }
}
