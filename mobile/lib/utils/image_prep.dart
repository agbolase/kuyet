import "dart:math" as math;
import "dart:typed_data";

import "package:image/image.dart" as img;

class InferenceViewBatch {
  InferenceViewBatch({
    required this.tensorBatch,
    required this.viewCount,
    required this.cropCount,
    required this.viewsPerCrop,
    required this.crops,
  });

  final Float32List tensorBatch;
  final int viewCount;
  final int cropCount;
  final int viewsPerCrop;
  final List<img.Image> crops;
}

List<double> cropOffsets(int width, int height) {
  final ratio = math.max(width, height) / math.max(math.min(width, height), 1);
  if (ratio >= 1.35) {
    return [0.0, 0.5, 1.0];
  }
  return [0.5];
}

img.Image squareCropResize(img.Image source, int size, {double offset = 0.5}) {
  final width = source.width;
  final height = source.height;
  final side = math.min(width, height);
  int left = 0;
  int top = 0;
  if (width >= height) {
    left = ((width - side) * offset).round().clamp(0, width - side);
  } else {
    top = ((height - side) * offset).round().clamp(0, height - side);
  }
  final cropped = img.copyCrop(
    source,
    x: left,
    y: top,
    width: side,
    height: side,
  );
  return img.copyResize(
    cropped,
    width: size,
    height: size,
    interpolation: img.Interpolation.linear,
  );
}

Float32List _imageToFloatTensor(img.Image image) {
  final out = Float32List(image.width * image.height * 3);
  var i = 0;
  for (var y = 0; y < image.height; y++) {
    for (var x = 0; x < image.width; x++) {
      final p = image.getPixel(x, y);
      out[i++] = p.r.toDouble();
      out[i++] = p.g.toDouble();
      out[i++] = p.b.toDouble();
    }
  }
  return out;
}

InferenceViewBatch buildInferenceViews(
  img.Image decoded,
  int size, {
  bool useTta = true,
}) {
  final offsets = useTta ? cropOffsets(decoded.width, decoded.height) : [0.5];
  final crops = <img.Image>[];
  final tensors = <Float32List>[];
  for (final offset in offsets) {
    final crop = squareCropResize(decoded, size, offset: offset);
    crops.add(crop);
    tensors.add(_imageToFloatTensor(crop));
    if (useTta) {
      final flipped = img.flipHorizontal(crop);
      tensors.add(_imageToFloatTensor(flipped));
    }
  }
  final viewsPerCrop = useTta ? 2 : 1;
  final flat = Float32List(tensors.length * size * size * 3);
  for (var v = 0; v < tensors.length; v++) {
    flat.setRange(v * size * size * 3, (v + 1) * size * size * 3, tensors[v]);
  }
  return InferenceViewBatch(
    tensorBatch: flat,
    viewCount: tensors.length,
    cropCount: crops.length,
    viewsPerCrop: viewsPerCrop,
    crops: crops,
  );
}

List<double> selectBestPrediction(
  List<List<double>> viewProbabilities,
  int cropCount,
  int viewsPerCrop,
) {
  final classCount = viewProbabilities.first.length;
  final grouped = List.generate(cropCount, (_) => List.filled(classCount, 0.0));
  for (var c = 0; c < cropCount; c++) {
    for (var k = 0; k < classCount; k++) {
      var sum = 0.0;
      for (var v = 0; v < viewsPerCrop; v++) {
        sum += viewProbabilities[c * viewsPerCrop + v][k];
      }
      grouped[c][k] = sum / viewsPerCrop;
    }
  }
  var bestCrop = 0;
  var bestPeak = -1.0;
  for (var c = 0; c < cropCount; c++) {
    final peak = grouped[c].reduce(math.max);
    if (peak > bestPeak) {
      bestPeak = peak;
      bestCrop = c;
    }
  }
  return grouped[bestCrop];
}

List<double> sharpenProbabilities(List<double> probabilities, double temperature) {
  if (temperature <= 0 || temperature >= 1) {
    return List<double>.from(probabilities);
  }
  final logits = probabilities
      .map((p) => math.log(p.clamp(1e-8, 1.0)) / temperature)
      .toList();
  final maxLogit = logits.reduce(math.max);
  final exp = logits.map((l) => math.exp(l - maxLogit)).toList();
  final sum = exp.reduce((a, b) => a + b);
  return exp.map((e) => e / sum).toList();
}
