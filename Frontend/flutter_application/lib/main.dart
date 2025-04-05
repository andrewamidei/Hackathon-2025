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

    const Key centerKey = ValueKey<String>('bottom-sliver-list');

    return Scaffold(
      appBar: AppBar(
        title: Text('Flutter App with Python Backend'),
      ),
      body: CustomScrollView(
        center: centerKey,
        slivers: <Widget>[
          SliverList(
            key: centerKey,
            delegate: SliverChildBuilderDelegate(
            childCount: 1, // do not make any duplicates
              (BuildContext context, int index) {
                return SafeArea(
                  child: Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Column(
                      children: [
                        Center(
                          child: BlocBuilder<BackendBloc, String>(
                            builder: (context, state) {
                              return Text(state);
                            },
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
                            child: Text('Fetch Data from Python Backend'),
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              }
            ),
          ),
        ]
      )
    );
  }
}