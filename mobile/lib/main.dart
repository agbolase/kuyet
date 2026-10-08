import "package:flutter/material.dart";

import "data/model_metadata.dart";
import "screens/history_screen.dart";
import "screens/home_screen.dart";
import "screens/scan_screen.dart";
import "services/guide_service.dart";
import "services/history_service.dart";
import "services/inference_service.dart";
import "theme/tomato_theme.dart";

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const TomatoCareApp());
}

class TomatoCareApp extends StatefulWidget {
  const TomatoCareApp({super.key});

  @override
  State<TomatoCareApp> createState() => _TomatoCareAppState();
}

class _TomatoCareAppState extends State<TomatoCareApp> {
  int _tab = 0;
  ModelMetadata? _metadata;
  InferenceService? _inference;
  final _guides = GuideService();
  final _history = HistoryService();
  bool _modelReady = false;
  bool _booting = true;

  @override
  void initState() {
    super.initState();
    _bootstrap();
  }

  Future<void> _bootstrap() async {
    _modelReady = await InferenceService.hasBundledModel();
    final metadata = await ModelMetadata.load();
    await _guides.load();
    InferenceService? inference;
    if (_modelReady) {
      inference = InferenceService(metadata);
      await inference.init();
    }
    if (!mounted) {
      return;
    }
    setState(() {
      _metadata = metadata;
      _inference = inference;
      _booting = false;
    });
  }

  @override
  void dispose() {
    _inference?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "TomatoCare",
      debugShowCheckedModeBanner: false,
      theme: TomatoTheme.dark(),
      home: _booting
          ? const Scaffold(
              body: Center(child: CircularProgressIndicator()),
            )
          : Scaffold(
              appBar: AppBar(
                title: const Text("🍅 TomatoCare"),
                centerTitle: false,
              ),
              body: IndexedStack(
                index: _tab,
                children: [
                  HomeScreen(onScanTap: () => setState(() => _tab = 1)),
                  ScanScreen(
                    metadata: _metadata!,
                    inference: _inference ?? InferenceService(_metadata!),
                    guides: _guides,
                    history: _history,
                    modelReady: _modelReady,
                  ),
                  HistoryScreen(history: _history),
                ],
              ),
              bottomNavigationBar: NavigationBar(
                selectedIndex: _tab,
                onDestinationSelected: (i) => setState(() => _tab = i),
                destinations: const [
                  NavigationDestination(
                    icon: Icon(Icons.home_outlined),
                    selectedIcon: Icon(Icons.home),
                    label: "Home",
                  ),
                  NavigationDestination(
                    icon: Icon(Icons.document_scanner_outlined),
                    selectedIcon: Icon(Icons.document_scanner),
                    label: "Scan",
                  ),
                  NavigationDestination(
                    icon: Icon(Icons.history),
                    selectedIcon: Icon(Icons.history),
                    label: "History",
                  ),
                ],
              ),
            ),
    );
  }
}
