import "dart:convert";
import "dart:io";

import "package:image/image.dart" as img;
import "package:intl/intl.dart";
import "package:path_provider/path_provider.dart";
import "package:uuid/uuid.dart";

class ScanHistoryEntry {
  ScanHistoryEntry({
    required this.id,
    required this.at,
    required this.predictedKey,
    required this.confidence,
    required this.displayName,
    required this.thumbPath,
  });

  final String id;
  final DateTime at;
  final String predictedKey;
  final double confidence;
  final String displayName;
  final String? thumbPath;

  factory ScanHistoryEntry.fromJson(Map<String, dynamic> json) {
    return ScanHistoryEntry(
      id: json["id"] as String,
      at: DateTime.parse(json["at"] as String),
      predictedKey: json["predicted_key"] as String,
      confidence: (json["confidence"] as num).toDouble(),
      displayName: json["display_name"] as String? ?? json["predicted_key"] as String,
      thumbPath: json["thumb_path"] as String?,
    );
  }

  Map<String, dynamic> toJson() => {
        "id": id,
        "at": at.toUtc().toIso8601String(),
        "predicted_key": predictedKey,
        "confidence": confidence,
        "display_name": displayName,
        if (thumbPath != null) "thumb_path": thumbPath,
      };
}

class HistoryService {
  static const _maxEntries = 500;
  Directory? _root;

  Future<Directory> rootDir() async {
    if (_root != null) {
      return _root!;
    }
    final docs = await getApplicationDocumentsDirectory();
    _root = Directory("${docs.path}/scan_logs");
    await _root!.create(recursive: true);
    await Directory("${_root!.path}/thumbs").create(recursive: true);
    return _root!;
  }

  Future<File> historyFile() async {
    final root = await rootDir();
    return File("${root.path}/history.json");
  }

  Future<List<ScanHistoryEntry>> load() async {
    final file = await historyFile();
    if (!await file.exists()) {
      return [];
    }
    try {
      final list = jsonDecode(await file.readAsString()) as List;
      return list
          .cast<Map<String, dynamic>>()
          .map(ScanHistoryEntry.fromJson)
          .toList();
    } on Object {
      return [];
    }
  }

  Future<void> save(List<ScanHistoryEntry> entries) async {
    final file = await historyFile();
    final payload = entries.map((e) => e.toJson()).toList();
    await file.writeAsString(jsonEncode(payload));
  }

  Future<ScanHistoryEntry> record({
    required String predictedKey,
    required double confidence,
    required String displayName,
    required img.Image crop,
  }) async {
    final id = const Uuid().v4();
    final root = await rootDir();
    final thumbRel = "thumbs/$id.jpg";
    final thumbFile = File("${root.path}/$thumbRel");
    final thumb = img.copyResize(crop, width: 120, height: 120);
    await thumbFile.writeAsBytes(img.encodeJpg(thumb, quality: 85));

    final entry = ScanHistoryEntry(
      id: id,
      at: DateTime.now(),
      predictedKey: predictedKey,
      confidence: confidence,
      displayName: displayName,
      thumbPath: thumbRel,
    );
    final entries = await load();
    entries.insert(0, entry);
    if (entries.length > _maxEntries) {
      entries.removeRange(_maxEntries, entries.length);
    }
    await save(entries);
    return entry;
  }

  Future<File?> thumbFileFor(ScanHistoryEntry entry) async {
    if (entry.thumbPath == null) {
      return null;
    }
    final root = await rootDir();
    final file = File("${root.path}/${entry.thumbPath}");
    if (await file.exists()) {
      return file;
    }
    return null;
  }

  String formatWhen(DateTime at) =>
      DateFormat.yMMMd().add_jm().format(at.toLocal());
}
