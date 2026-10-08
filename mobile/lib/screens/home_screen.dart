import "package:flutter/material.dart";

import "../theme/tomato_theme.dart";

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key, required this.onScanTap});

  final VoidCallback onScanTap;

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Spacer(flex: 2),
            Text.rich(
              TextSpan(
                style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      color: TomatoTheme.text,
                      fontWeight: FontWeight.w700,
                      height: 1.1,
                    ),
                children: const [
                  TextSpan(text: "Check Your "),
                  TextSpan(
                    text: "Tomato",
                    style: TextStyle(color: TomatoTheme.tomato),
                  ),
                  TextSpan(text: " Leaf"),
                ],
              ),
            ),
            const SizedBox(height: 12),
            Text(
              "Take or upload a picture of a tomato leaf to check for common "
              "signs of disease. Works fully offline on your phone.",
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    color: TomatoTheme.muted,
                    height: 1.45,
                  ),
            ),
            const SizedBox(height: 24),
            FilledButton.icon(
              onPressed: onScanTap,
              icon: const Icon(Icons.photo_camera_outlined),
              label: const Text("Scan a Leaf"),
            ),
            const Spacer(flex: 3),
            const Divider(color: Color(0x22FFFFFF)),
            const SizedBox(height: 12),
            Text(
              "Contact",
              style: Theme.of(context).textTheme.titleSmall?.copyWith(
                    color: TomatoTheme.text,
                    fontWeight: FontWeight.w600,
                  ),
            ),
            const SizedBox(height: 6),
            Text(
              "Questions or feedback? Contact your extension officer or "
              "project maintainer.",
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: TomatoTheme.muted,
                    height: 1.4,
                  ),
            ),
            const SizedBox(height: 8),
          ],
        ),
      ),
    );
  }
}
