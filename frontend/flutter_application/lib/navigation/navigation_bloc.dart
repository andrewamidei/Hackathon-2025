import 'package:flutter_bloc/flutter_bloc.dart';
//import 'package:flutter/material.dart';

enum BottomNaviEvent{ home, settings, chat }

class BottomNaviBloc extends Bloc<BottomNaviEvent, int>{
  BottomNaviBloc() : super (0) {
    on<BottomNaviEvent>((event, emit) {
      switch (event) {
        case BottomNaviEvent.home:
          emit(0);
          break;
        case BottomNaviEvent.settings:
          emit(1);
          break;
        case BottomNaviEvent.chat:
          emit(2);
          break;
      }
    });
  }
}