import 'package:flutter/material.dart';
import 'package:flutter_application/chat/chat_page.dart';
import 'package:flutter_application/login/login_page.dart';
import 'package:flutter_application/settings/settings_page.dart';
import 'package:flutter_application/contacts/contacts_page.dart'; // Add this import
import 'package:flutter_bloc/flutter_bloc.dart';
import 'navigation_bloc.dart';

class NavigationPage extends StatelessWidget{
  final String username;

  const NavigationPage ({
    super.key,
    required this.username,
  });
  
@override
Widget build(BuildContext context){
  return MaterialApp(
    debugShowCheckedModeBanner: false,
    home: BlocProvider(
      create: (context) => BottomNaviBloc(),
      child: MyHome(username: username),
      ),
    );
  }
}

// This code normally goes in a page with "view" at the end of it rather than page and the stuff above stays
class MyHome extends StatelessWidget {
  final String username;  // Add this

  const MyHome({
    super.key,
    required this.username,  // Add this
  });

  @override
  Widget build(BuildContext context) {
    final bottomNaviBloc = BlocProvider.of<BottomNaviBloc>(context);

    return LayoutBuilder(
      builder: (context, constraints) {
        return Scaffold(
          body: BlocBuilder<BottomNaviBloc, int>(
            builder: (context, currentIndex) {
              switch(currentIndex) {
                case 0:
                  return const LoginPage();
                case 1:
                  return ContactsPage(
                    currentUser: username,  // Use actual username
                  );
                case 2:
                  return const SettingsPage();
                // case 3:
                //   return ChatPage(
                //     currentUser: username,  // Use actual username
                //     receiver: 'bob',  // This should be set when selecting a contact
                //   );
                default:
                  return const Placeholder();
              }
            },
          ),
          bottomNavigationBar: BottomNavigationBar(
            // currentIndex: currentIndex,
            onTap: (index) => bottomNaviBloc.add(BottomNaviEvent.values[index]),
            items: const [
                BottomNavigationBarItem(
                icon: Icon(Icons.login),
                label: 'Login',
                ),
                BottomNavigationBarItem(
                icon: Icon(Icons.contacts),
                label: 'Contacts',
                ),
                BottomNavigationBarItem(
                icon: Icon(Icons.settings),
                label: 'Settings',
                ),
            ],
            ),
        );
      }
    );
  }
}
