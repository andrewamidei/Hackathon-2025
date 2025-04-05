import 'package:flutter/material.dart';
import 'package:flutter_application/chat/chat_page.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'login_bloc.dart';


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
        final loginBloc = BlocProvider.of<LoginBloc>(context);
        String username = "";
        String password = "";

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
              onChanged: (value) {
                username = value;
              }
            ),
            const SizedBox(height: 16.0),

            // Password TextField
            TextField(
              decoration: const InputDecoration(
                labelText: 'Password',
                border: OutlineInputBorder(),
              ),
              obscureText: true,
              onChanged: (value) {
                password = value;
              },
            ),
            const SizedBox(height: 24.0),

            // Login Button
            ElevatedButton(
            onPressed: () async {
                // Check if username or password is empty
                if (username.isEmpty || password.isEmpty) {
                // Show an error message using a SnackBar
                ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                    content: Text('Please enter both username and password'),
                    backgroundColor: Colors.red,
                    ),
                );
                } else {
                // Proceed with login logic
                final isValid = await loginBloc.verifyUser(username, password);
                    if (!isValid) {
                        // Show an error message if username or password is incorrect
                        ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                                content: Text('Username or password is incorrect'),
                                backgroundColor: Colors.red,
                            ),
                        );
                    } else {
                        Navigator.push(
                            context,
                            MaterialPageRoute(builder: (context) => const ChatPage()),
                        );
                    }
                }
            },
            child: const Text('Login'),
            ),
          ],
        ),
      ),
    );
    }
}