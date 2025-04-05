import 'package:flutter/material.dart';

class ThemeState {
  final ThemeData themeData;

  ThemeState(this.themeData);

  static ThemeState get darkTheme =>
      ThemeState(ThemeData.dark().copyWith(
        // Customize dark theme properties
      ));

  static ThemeState get lightTheme =>
      ThemeState(ThemeData.light().copyWith(
        // Customize light theme properties
      ));
}