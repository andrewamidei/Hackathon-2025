import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import "chat_bloc.dart";

class ChatPage extends StatelessWidget {
  const ChatPage({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => BackendBloc(),
      child: ChatView(),
    );
  }
}

class ChatView extends StatelessWidget {
  const ChatView({super.key});

  @override
  Widget build(BuildContext context) {
    final backendBloc = BlocProvider.of<BackendBloc>(context);

    return Scaffold(
      appBar: AppBar(
        title: Text('Flutter App with Python Backend'),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(12.0),
          child: Column(
            children: [
              Expanded(
                child: CustomScrollView(
                  scrollDirection: Axis.vertical,
                  shrinkWrap: true,
                  slivers: <Widget>[
                    SliverList(
                      delegate: SliverChildBuilderDelegate(
                      childCount: 1, // make 1 copy of everything
                        (BuildContext context, int index) {
                          return BlocBuilder<BackendBloc, String>(
                            builder: (context, state) {
                              return Text(state);
                            },
                          );
                        }
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 20),
              SizedBox(
                // width: 370,
                child: TextField(
                  // controller: nameController,
                  decoration: InputDecoration(
                    border: OutlineInputBorder(),
                    labelText: '',
                  ),
                ),
              ),
              const SizedBox(height: 20),
              Center(
                child: ElevatedButton(
                  onPressed: () {
                    // backendBloc.fetchData();
                    backendBloc.sendData("Tell me a story");
                  },
                  child: Text('Send Message'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}