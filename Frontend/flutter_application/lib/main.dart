import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import "backend_bloc.dart";

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: BlocProvider(
        create: (context) => BackendBloc(),
        child: MyWidget(),
      ),
    );
  }
}

class MyWidget extends StatelessWidget {
  const MyWidget({super.key});

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