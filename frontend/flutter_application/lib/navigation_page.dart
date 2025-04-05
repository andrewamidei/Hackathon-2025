// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables, avoid_print

import 'package:flutter/material.dart';

class NavPage extends StatefulWidget {
  const NavPage({super.key});

  @override
  State<NavPage> createState() => _NavPageState(); // underscore in the widget makes the class private
}

class _NavPageState extends State<NavPage> {
  var selectedIndex = 0;

  void onItemTapped(int index) {
    setState(() {
      selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {

    Widget page;
    switch (selectedIndex) {
      case 0:
        page = Placeholder(); // a placeholder for a new widget witch hasn't been created
      case 1:
        page = Placeholder(); 
      case 2:
        page = Placeholder(); 
      default:
        throw UnimplementedError('no widget for $selectedIndex');
    }

    return LayoutBuilder(
      builder: (context, constraints) {
        return Scaffold(
          floatingActionButton: FloatingActionButton(
            child: Icon(Icons.play_arrow),
            onPressed:() {
              Placeholder;
            },
          ),
          bottomNavigationBar: BottomNavigationBar(
                items: const <BottomNavigationBarItem>[
                  BottomNavigationBarItem(
                    icon: Icon(Icons.home),
                    label: 'Home',
                  ),
                  BottomNavigationBarItem(
                    icon: Icon(Icons.local_dining),
                    label: 'Recipe',
                  ),
                  BottomNavigationBarItem(
                    icon: Icon(Icons.menu),
                    label: 'Menu',
                  ),
                ],
                currentIndex: selectedIndex,
                onTap: onItemTapped,
          ),
          body: page,  // variable that stores what page you see
        );
      }
    );
  }
}
