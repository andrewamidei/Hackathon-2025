import 'package:flutter/material.dart';
import 'package:flutter_application/chat/chat_bloc.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import "login_bloc.dart";


class LoginPage extends StatelessWidget {
    const LoginPage({
        super.key,
    });

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
        create: (context) => LoginBloc(),
        child: LoginView(),
    );
  }
}


class LoginView extends StatelessWidget {
    const LoginView({super.key});

    @override
    Widget build(BuildContext context) {
        final backendBloc = BlocProvider.of<LoginBloc>(context);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Email TextField
            TextField(
              decoration: const InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
              ),
              keyboardType: TextInputType.emailAddress,
            ),
            const SizedBox(height: 16.0),

            // Password TextField
            TextField(
              decoration: const InputDecoration(
                labelText: 'Password',
                border: OutlineInputBorder(),
              ),
              obscureText: true,
            ),
            const SizedBox(height: 24.0),

            // Login Button
            ElevatedButton(
              onPressed: () {
                // Add login logic here
                // backendBloc.add(LoginEvent());
              },
              child: const Text('Login'),
            ),
          ],
        ),
      ),
    );
    }
}