import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'settings_bloc.dart';

class SettingsPage extends StatelessWidget{
    const SettingsPage({
        super.key,
    });

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
        create: (context) => SettingsBloc(),
        child: settingsView(),
    );
  }
}
class settingsView extends StatelessWidget {
@override
    Widget build(BuildContext context) {
        final loginBloc = BlocProvider.of<SettingsBloc>(context);
    return Scaffold(
      appBar: AppBar(title: const Text('Settings'),),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column( 
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(decoration: const InputDecoration(
            labelText: 'Server Address',


            ),)
          ],
        ),
        

      ),


    );
  }
}



