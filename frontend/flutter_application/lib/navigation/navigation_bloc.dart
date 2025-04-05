import 'package:flutter_bloc/flutter_bloc.dart';
//import 'package:flutter/material.dart';

enum BottomNaviEvent{chat, contacts, settings, login}

class BottomNaviBloc extends Bloc<BottomNaviEvent, int>{
  BottomNaviBloc() : super (0) {
    on<BottomNaviEvent>((event, emit) {
      switch (event) {
        case BottomNaviEvent.chat:
          emit(0);
          break;
        case BottomNaviEvent.contacts:
          emit(1);
          break;
        case BottomNaviEvent.settings:
          emit(2);
          break;
        case BottomNaviEvent.login:
          emit(3);
          break;
      }
    });
  }
}