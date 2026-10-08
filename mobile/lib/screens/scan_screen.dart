import "dart:typed_data";

import "package:flutter/material.dart";
import "package:image/image.dart" as img;
import "package:image_picker/image_picker.dart";

import "../data/model_metadata.dart";
import "../services/guide_service.dart";
import "../services/history_service.dart";
import "../services/inference_service.dart";
import "../theme/tomato_theme.dart";

class ScanScreen extends StatefulWidget {
  const ScanScreen({
    super.key,
    required this.metadata,
    required this.inference,
    required this.guides,
    required this.history,
    required this.modelReady,
  });

  final ModelMetadata metadata;
  final InferenceService inference;
  final GuideService guides;
  final HistoryService history;
  final bool modelReady;

  @override
  State<ScanScreen> createState() => _ScanScreenState();
}

class _ScanScreenState extends State<ScanScreen> {
  final _picker = ImagePicker();
  Uint8List? _bytes;
  ScanOutcome? _outcome;
  bool _busy = false;
  bool _useTta = true;
  String _lang = "en";

  Future<void> _pick(ImageSource source) async {
    final file = await _picker.pickImage(source: source, imageQuality: 92);
    if (file == null) {
      return;
    }
    final bytes = await file.readAsBytes();
    setState(() {
      _bytes = bytes;
      _outcome = null;
    });
  }

  Future<void> _analyze() async {
    if (_bytes == null || !widget.modelReady) {
      return;
    }
    setState(() => _busy = true);
    try {
      final outcome = await widget.inference.analyze(_bytes!, useTta: _useTta);
      final display = widget.metadata.displayNames[outcome.predictedKey] ??
          outcome.predictedKey.replaceAll("_", " ");
      await widget.history.record(
        predictedKey: outcome.predictedKey,
        confidence: outcome.confidence,
        displayName: display,
        crop: outcome.bestCrop,
      );
      if (!mounted) {
        return;
      }
      setState(() => _outcome = outcome);
    } catch (error) {
      if (!mounted) {
        return;
      }
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Scan failed: $error")),
      );
    } finally {
      if (mounted) {
        setState(() => _busy = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (!widget.modelReady) {
      return SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                "Model not bundled",
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      color: TomatoTheme.text,
                    ),
              ),
              const SizedBox(height: 12),
              Text(
                "Export hortivision_model.tflite (and optional gate files) "
                "into mobile/assets/models, then rebuild the APK.",
                style: const TextStyle(color: TomatoTheme.muted, height: 1.45),
              ),
            ],
          ),
        ),
      );
    }

    return SafeArea(
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "Scan a tomato leaf",
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                            color: TomatoTheme.text,
                            fontWeight: FontWeight.w600,
                          ),
                    ),
                    const SizedBox(height: 4),
                    const Text(
                      "Camera or gallery · offline inference",
                      style: TextStyle(color: TomatoTheme.muted, fontSize: 13),
                    ),
                  ],
                ),
              ),
              OutlinedButton(
                onPressed: () => setState(
                  () => _lang = _lang == "en" ? "ha" : "en",
                ),
                child: Text(_lang == "en" ? "Hausa" : "English"),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: _busy ? null : () => _pick(ImageSource.camera),
                  icon: const Icon(Icons.photo_camera_outlined),
                  label: const Text("Camera"),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: _busy ? null : () => _pick(ImageSource.gallery),
                  icon: const Icon(Icons.photo_library_outlined),
                  label: const Text("Gallery"),
                ),
              ),
            ],
          ),
          SwitchListTile(
            contentPadding: EdgeInsets.zero,
            title: const Text(
              "Extra accuracy (multi-crop)",
              style: TextStyle(color: TomatoTheme.text),
            ),
            value: _useTta,
            onChanged: _busy ? null : (v) => setState(() => _useTta = v),
          ),
          if (_bytes != null) ...[
            const SizedBox(height: 8),
            ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: Image.memory(_bytes!, fit: BoxFit.cover),
            ),
            const SizedBox(height: 12),
            FilledButton(
              onPressed: _busy ? null : _analyze,
              child: _busy
                  ? const SizedBox(
                      height: 22,
                      width: 22,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Text("Analyze leaf"),
            ),
          ],
          if (_outcome != null) ...[
            const SizedBox(height: 20),
            _ResultCard(
              outcome: _outcome!,
              metadata: widget.metadata,
              guides: widget.guides,
              lang: _lang,
            ),
          ],
        ],
      ),
    );
  }
}

class _ResultCard extends StatelessWidget {
  const _ResultCard({
    required this.outcome,
    required this.metadata,
    required this.guides,
    required this.lang,
  });

  final ScanOutcome outcome;
  final ModelMetadata metadata;
  final GuideService guides;
  final String lang;

  @override
  Widget build(BuildContext context) {
    final key = outcome.predictedKey;
    final guide = guides.guideFor(key, lang: lang);
    final name = lang == "ha"
        ? guide.name
        : (metadata.displayNames[key] ?? guide.name);
    final confidence = outcome.confidence;

    return Card(
      color: const Color(0xFF0C1C16),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(8),
              child: Image.memory(
                Uint8List.fromList(img.encodeJpg(outcome.bestCrop)),
                fit: BoxFit.cover,
              ),
            ),
            const SizedBox(height: 12),
            Text(
              name,
              style: const TextStyle(
                color: TomatoTheme.green,
                fontSize: 20,
                fontWeight: FontWeight.w700,
              ),
            ),
            const SizedBox(height: 8),
            LinearProgressIndicator(value: confidence.clamp(0, 1)),
            const SizedBox(height: 6),
            Text(
              "Confidence: ${(confidence * 100).toStringAsFixed(1)}%",
              style: const TextStyle(color: TomatoTheme.muted),
            ),
            if (confidence < 0.5) ...[
              const SizedBox(height: 8),
              const Text(
                "Low confidence — treat as tentative.",
                style: TextStyle(color: TomatoTheme.tomato),
              ),
            ],
            const SizedBox(height: 16),
            Text(
              guide.summary,
              style: const TextStyle(color: TomatoTheme.text, height: 1.45),
            ),
            if (guide.traits.isNotEmpty) ...[
              const SizedBox(height: 12),
              const Text(
                "What to look for",
                style: TextStyle(
                  color: TomatoTheme.text,
                  fontWeight: FontWeight.w600,
                ),
              ),
              for (final t in guide.traits)
                Text("• $t", style: const TextStyle(color: TomatoTheme.muted)),
            ],
            if (guide.prevention.isNotEmpty) ...[
              const SizedBox(height: 12),
              const Text(
                "Prevention",
                style: TextStyle(
                  color: TomatoTheme.text,
                  fontWeight: FontWeight.w600,
                ),
              ),
              for (final p in guide.prevention)
                Text("• $p", style: const TextStyle(color: TomatoTheme.muted)),
            ],
          ],
        ),
      ),
    );
  }
}
