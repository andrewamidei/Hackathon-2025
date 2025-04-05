import 'dart:convert';

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:http/http.dart' as http;

class LoginBloc extends Cubit<String> {
  LoginBloc() : super('');
  String username = '';

  Future<String?> verifyUser(String username, String password) async {
    const String url = 'http://192.168.8.137:8080/api/login';
    try {
      final response = await http.post(
        Uri.parse(url),
        headers: <String, String>{'Content-Type': 'application/json'},
        body: jsonEncode(<String, dynamic>{
          'username': username,
          'password': password,
        }),
      );
      if (response.statusCode == 200) {
        final Map<String, dynamic> responseBody = jsonDecode(response.body);
        final String? extractedUsername = responseBody['response']['username'];
        username = extractedUsername!;
        return extractedUsername;
        // Map<String, dynamic> map = jsonDecode(response.body);

        // emit(response.body);
      } else {
        return null;
      }
    } catch (e) {
      print(e);
      return null;
    }
  }

  void setUserName(String newUsername) {
    username = newUsername;
    emit(username);
  }

  String get currentUsername => username;

  Future<String?> signUpUser(String username, String password) async {
    const String url = 'http://192.168.8.137:8080/api/signup';
    try {
      final response = await http.post(
        Uri.parse(url),
        headers: <String, String>{'Content-Type': 'application/json'},
        body: jsonEncode(<String, dynamic>{
          'username': username,
          'password': password,
        }),
      );
      if (response.statusCode == 200) {
        final Map<String, dynamic> responseBody = jsonDecode(response.body);
        final String? extractedUsername = responseBody['response']['username'];
        username = extractedUsername!;
        return extractedUsername;
        // Map<String, dynamic> map = jsonDecode(response.body);
        // emit(response.body);
      } else {
        return null;
      }
    } catch (e) {
      print(e);
      return null;
    }
  }
}
