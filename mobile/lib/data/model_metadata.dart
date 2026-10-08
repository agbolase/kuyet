import "dart:convert";

import "package:flutter/services.dart";

class ModelMetadata {
  ModelMetadata({
    required this.classes,
    required this.displayNames,
    required this.imageSize,
  });

  final List<String> classes;
  final Map<String, String> displayNames;
  final int imageSize;

  static Future<ModelMetadata> load() async {
    final raw = await rootBundle.loadString("assets/models/class_names.json");
    final map = jsonDecode(raw) as Map<String, dynamic>;
    final classes = (map["classes"] as List).cast<String>();
    final names = (map["display_names"] as Map?)?.map(
          (k, v) => MapEntry(k.toString(), v.toString()),
        ) ??
        {};
    final size = (map["image_size"] as num?)?.toInt() ?? 224;
    return ModelMetadata(
      classes: classes,
      displayNames: names,
      imageSize: size,
    );
  }
}
