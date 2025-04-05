import 'package:flutter_bloc/flutter_bloc.dart';

enum BottomNaviEvent {
  login,
  contacts,
  settings,
  chat,
}

class BottomNaviBloc extends Bloc<BottomNaviEvent, int> {
  BottomNaviBloc() : super(0) {
    on<BottomNaviEvent>((event, emit) {
      switch (event) {
        case BottomNaviEvent.login:
          emit(0);
        case BottomNaviEvent.contacts:
          emit(1);
        case BottomNaviEvent.settings:
          emit(2);
        case BottomNaviEvent.chat:
          emit(3);
      }
    });
  }
}