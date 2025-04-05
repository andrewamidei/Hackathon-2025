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
      create: (context) => ChatBloc(),
      child: ChatView(),
    );
  }
}


// This code normally goes in a page with "view" at the end of it rather than page and the stuff above stays
class ChatView extends StatelessWidget {
  const ChatView({super.key});

  @override
  Widget build(BuildContext context) {
    final backendBloc = BlocProvider.of<ChatBloc>(context);

    return Scaffold(
      appBar: AppBar(
        title: Text('{User}'),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(10),
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
                          return BlocBuilder<ChatBloc, String>(
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
              Expanded(
                child: Row(
                  children: [
                    Expanded(
                      child: TextField(
                        //controller: ,
                        decoration: InputDecoration(
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(20),
                            borderSide: BorderSide(
                                width: 2,
                                style: BorderStyle.none,
                            ),
                          ),
                          labelText: 'message',
                        ),
                      ),
                    ),
                    SizedBox(width: 10),
                    IconButton(
                      icon: Icon(Icons.send, color: Colors.white,),
                      style: IconButton.styleFrom(backgroundColor: Colors.deepPurple),
                      onPressed: () {
                        backendBloc.sendData("hey how are you doing?");
                      },
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}