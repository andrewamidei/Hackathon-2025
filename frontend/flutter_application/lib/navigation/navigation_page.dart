
import 'package:flutter/material.dart';
import 'package:flutter_application/chat/chat_page.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'navigation_bloc.dart';

class NavigationPage extends StatelessWidget{
  const NavigationPage ({super.key});
  
@override
Widget build(BuildContext context){
  return MaterialApp(
    debugShowCheckedModeBanner: false,
    home: BlocProvider(
      create: (context) => BottomNaviBloc(),
      child: const MyHome(),
      ),
    );
  }
}

// This code normally goes in a page with "view" at the end of it rather than page and the stuff above stays
class MyHome extends StatelessWidget{
  const MyHome({super.key});
  
  @override
  Widget build(BuildContext context){
    final bottomNaviBloc = BlocProvider.of<BottomNaviBloc>(context);

    return LayoutBuilder(
      builder: (context, constraints) {
        return Scaffold(
          body: BlocBuilder<BottomNaviBloc,int>(
            builder: (context, currentIndex){
              switch(currentIndex){
                case 0:
                  return ChatPage();
                case 1:
                  return Placeholder();
                case 2: 
                  return Placeholder();
                case 3: 
                  return Placeholder();
                default:
                  return Placeholder();
              }
            },
          ),
          bottomNavigationBar: BlocBuilder<BottomNaviBloc, int>(
            builder: (context, currentIndex) {
              return BottomNavigationBar(
                currentIndex: currentIndex,
                onTap: (index) => bottomNaviBloc.add(BottomNaviEvent.values[index]),
                items: const [
                  BottomNavigationBarItem(
                    icon: Icon(Icons.message_rounded),
                    label: "Chat",
                  ),
                  // BottomNavigationBarItem(
                  //   icon: Icon(Icons.person),
                  //   label: "Contacts",
                  // ),
                  BottomNavigationBarItem(
                    icon: Icon(Icons.settings),
                    label: "Settings",
                  ),
                  BottomNavigationBarItem(
                    icon: Icon(Icons.login),
                    label: "Login",
                  ),
                ],
              );
            }
          )
        );
      }
    );
  }
}