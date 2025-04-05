import 'dart:convert';

import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:http/http.dart' as http;

class LoginBloc extends Cubit<String> {
  LoginBloc() : super('');

  Future<bool> verifyUser(String username, String password ) async {
    const String url = 'http://192.168.8.137:8080/api/login';
    try {
        final response = await http.post(
            Uri.parse(url),
            headers:<String, String>{'Content-Type': 'application/json'},
            body: jsonEncode(<String, dynamic>{'username': username, 'password': password})
        );
        if (response.statusCode == 200) {
            // Map<String, dynamic> map = jsonDecode(response.body);
            return true;
            // emit(response.body);
        } else {
            return false;
        }
    } catch(e) {
        print(e);
        return false;
    }
  } 

  Future<bool> signUpUser(String username, String password ) async {
    const String url = 'http://192.168.8.137:8080/api/signup';
    try {
        final response = await http.post(
            Uri.parse(url),
            headers:<String, String>{'Content-Type': 'application/json'},
            body: jsonEncode(<String, dynamic>{'username': username, 'password': password})
        );
        if (response.statusCode == 200) {
            // Map<String, dynamic> map = jsonDecode(response.body);
            return true;
            // emit(response.body);
        } else {
            return false;
        }
    } catch(e) {
        print(e);
        return false;
    }
  } 
}