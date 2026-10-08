import "package:flutter/material.dart";

abstract final class TomatoTheme {
  static const green = Color(0xFF3DDC84);
  static const greenDark = Color(0xFF2BB86A);
  static const tomato = Color(0xFFE06B5A);
  static const bg = Color(0xFF071410);
  static const text = Color(0xFFE8F5EC);
  static const muted = Color(0xFF8FA89A);

  static ThemeData dark() {
    const scheme = ColorScheme.dark(
      primary: green,
      secondary: tomato,
      surface: Color(0xFF0C1C16),
      onPrimary: Color(0xFF04210F),
      onSurface: text,
    );
    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      scaffoldBackgroundColor: bg,
      appBarTheme: const AppBarTheme(
        backgroundColor: Color(0xCC071410),
        foregroundColor: text,
        elevation: 0,
      ),
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: const Color(0xE6071410),
        indicatorColor: green.withValues(alpha: 0.2),
        labelTextStyle: WidgetStateProperty.resolveWith(
          (states) => TextStyle(
            fontSize: 12,
            color: states.contains(WidgetState.selected) ? green : muted,
          ),
        ),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: green,
          foregroundColor: const Color(0xFF04210F),
          minimumSize: const Size.fromHeight(48),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(999),
          ),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: text,
          minimumSize: const Size.fromHeight(48),
          side: BorderSide(color: muted.withValues(alpha: 0.35)),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(999),
          ),
        ),
      ),
    );
  }
}
