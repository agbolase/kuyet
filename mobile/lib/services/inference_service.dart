import "package:flutter/services.dart";
import "package:image/image.dart" as img;
import "package:tflite_flutter/tflite_flutter.dart";

import "../data/model_metadata.dart";
import "../utils/image_prep.dart";

class ScanOutcome {
  ScanOutcome({
    required this.predictedKey,
    required this.confidence,
    required this.probabilities,
    required this.topIndices,
    required this.bestCrop,
  });

  final String predictedKey;
  final double confidence;
  final List<double> probabilities;
  final List<int> topIndices;
  final img.Image bestCrop;
}

class InferenceService {
  InferenceService(this.metadata);

  final ModelMetadata metadata;
  Interpreter? _interpreter;
  static const _modelAsset = "assets/models/hortivision_model.tflite";
  static const _softmaxTemperature = 0.45;

  static Future<bool> hasBundledModel() async {
    try {
      await rootBundle.load(_modelAsset);
      return true;
    } on Object {
      return false;
    }
  }

  Future<void> init() async {
    if (_interpreter != null) {
      return;
    }
    _interpreter = await Interpreter.fromAsset(_modelAsset);
  }

  Future<ScanOutcome> analyze(Uint8List bytes, {bool useTta = true}) async {
    await init();
    final interpreter = _interpreter!;
    final decoded = img.decodeImage(bytes);
    if (decoded == null) {
      throw const FormatException("Could not decode image");
    }
    final batch = buildInferenceViews(
      decoded,
      metadata.imageSize,
      useTta: useTta,
    );
    final classCount = metadata.classes.length;
    final viewProbabilities = <List<double>>[];
    final size = metadata.imageSize;
    final plane = size * size * 3;

    for (var v = 0; v < batch.viewCount; v++) {
      final slice = batch.tensorBatch.sublist(v * plane, (v + 1) * plane);
      final input = _toInput4d(slice, size);
      final output = List<List<double>>.generate(
        1,
        (_) => List<double>.filled(classCount, 0),
      );
      interpreter.run(input, output);
      viewProbabilities.add(List<double>.from(output.first));
    }

    var probabilities = selectBestPrediction(
      viewProbabilities,
      batch.cropCount,
      batch.viewsPerCrop,
    );
    probabilities = sharpenProbabilities(probabilities, _softmaxTemperature);

    final indexed = List.generate(classCount, (i) => i)
      ..sort((a, b) => probabilities[b].compareTo(probabilities[a]));
    final top = indexed.take(3).toList();
    final predicted = top.first;
    final bestCropIndex = _bestCropIndex(viewProbabilities, batch);
    return ScanOutcome(
      predictedKey: metadata.classes[predicted],
      confidence: probabilities[predicted],
      probabilities: probabilities,
      topIndices: top,
      bestCrop: batch.crops[bestCropIndex],
    );
  }

  List<List<List<List<double>>>> _toInput4d(List<double> flat, int size) {
    final out = List.generate(
      1,
      (_) => List.generate(
        size,
        (y) => List.generate(
          size,
          (x) {
            final base = (y * size + x) * 3;
            return [
              flat[base],
              flat[base + 1],
              flat[base + 2],
            ];
          },
        ),
      ),
    );
    return out;
  }

  int _bestCropIndex(
    List<List<double>> viewProbabilities,
    InferenceViewBatch batch,
  ) {
    var bestCrop = 0;
    var bestPeak = -1.0;
    for (var c = 0; c < batch.cropCount; c++) {
      var peak = -1.0;
      for (var v = 0; v < batch.viewsPerCrop; v++) {
        final row = viewProbabilities[c * batch.viewsPerCrop + v];
        for (final value in row) {
          if (value > peak) {
            peak = value;
          }
        }
      }
      if (peak > bestPeak) {
        bestPeak = peak;
        bestCrop = c;
      }
    }
    return bestCrop;
  }

  void dispose() {
    _interpreter?.close();
    _interpreter = null;
  }
}
