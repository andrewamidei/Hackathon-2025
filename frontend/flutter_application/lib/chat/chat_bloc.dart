import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

// const String url = 'http://192.168.8.137:8080/api/queryllm';
const String url = 'http://localhost:8080/api/queryllm';

class ChatBloc extends Cubit<String> {
  ChatBloc() : super('');

  TextEditingController messageController = TextEditingController();

  Future<void> sendData(/*String prompt*/) async {
    String prompt = messageController.text;
    if (prompt.isNotEmpty) { 
      try {
        
        final response = await http.post(
          Uri.parse(url),
          headers:<String, String>{'Content-Type': 'application/json'},
          body: jsonEncode(<String, dynamic>{'model': 'smollm2:135m', 'prompt': prompt}));

          if (response.statusCode == 200) {
            Map<String, dynamic> map = jsonDecode(response.body);
            emit(map["response"]);
            // emit(response.body);
          } else {
            emit('Failed to fetch data');
          }
      }
      catch (e) {
        emit('Failed to connect to the server.');
      }
      messageController.clear(); // Clear the text field after sending
    }
  }

  Future<void> message(TextEditingController prompt) async {

  }
}


// import 'package:flutter_bloc/flutter_bloc.dart';
// import 'package:http/http.dart' as http;
// import 'dart:convert';

// class BackendBloc extends Cubit<String> {
//   BackendBloc() : super('');

//   Future<void> fetchData() async {
//     final response = await http.get(Uri.parse('http://localhost:5000/api/data'));
//     if (response.statusCode == 200) {
//       emit(response.body);
//     } else {
//       emit('Failed to fetch data');
//     }
//   }

//   Future<void> sendData(String prompt) async {
//     // just finished making this
//     try {
//       final response = await http.post(
//         Uri.parse('http://localhost:5000/api/data'),
//         headers:<String, String>{'Content-Type': 'application/json'},
//         body: jsonEncode(<String, dynamic>{'model': 'smollm2:135m', 'prompt': prompt}));

//         if (response.statusCode == 200) {
//           Map<String, dynamic> map = jsonDecode(response.body);
//           emit(map["response"]);
//           // emit(response.body);
//         } else {
//           emit('Failed to fetch data');
//         }
//     }
//     catch (e) {
//       emit('Failed to connect to the server.');
//     }
//   }
// }