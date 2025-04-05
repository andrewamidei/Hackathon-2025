
import 'package:flutter/material.dart';
import 'package:flutter_application/chat/chat_page.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'navigation_bloc.dart';


void main(){
  runApp(const NavigationPage());
}

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
        appBar: AppBar(
          title: Text("Bottom naviagtion bar"),
        ),
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
                  icon: Icon(
                    Icons.login,
                  ),
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

// // ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables, avoid_print

// import 'package:flutter/material.dart';

// class NavPage extends StatefulWidget {
//   const NavPage({super.key});

//   @override
//   State<NavPage> createState() => _NavPageState(); // underscore in the widget makes the class private
// }

// class _NavPageState extends State<NavPage> {
//   var selectedIndex = 0;

//   void onItemTapped(int index) {
//     setState(() {
//       selectedIndex = index;
//     });
//   }

//   @override
//   Widget build(BuildContext context) {

//     Widget page;
//     switch (selectedIndex) {
//       case 0:
//         page = Placeholder(); // a placeholder for a new widget witch hasn't been created
//       case 1:
//         page = Placeholder(); 
//       case 2:
//         page = Placeholder(); 
//       default:
//         throw UnimplementedError('no widget for $selectedIndex');
//     }

//     return LayoutBuilder(
//       builder: (context, constraints) {
//         return Scaffold(
//           floatingActionButton: FloatingActionButton(
//             child: Icon(Icons.play_arrow),
//             onPressed:() {
//               Placeholder;
//             },
//           ),
//           bottomNavigationBar: BottomNavigationBar(
//                 items: const <BottomNavigationBarItem>[
//                   BottomNavigationBarItem(
//                     icon: Icon(Icons.home),
//                     label: 'Home',
//                   ),
//                   BottomNavigationBarItem(
//                     icon: Icon(Icons.local_dining),
//                     label: 'Recipe',
//                   ),
//                   BottomNavigationBarItem(
//                     icon: Icon(Icons.menu),
//                     label: 'Menu',
//                   ),
//                 ],
//                 currentIndex: selectedIndex,
//                 onTap: onItemTapped,
//           ),
//           body: page,  // variable that stores what page you see
//         );
//       }
//     );
//   }
// }
