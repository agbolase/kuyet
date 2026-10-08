import "dart:convert";

import "package:flutter/services.dart";

class DiseaseGuide {
  DiseaseGuide({
    required this.name,
    required this.agentType,
    required this.agent,
    required this.summary,
    required this.traits,
    required this.prevention,
  });

  final String name;
  final String agentType;
  final String agent;
  final String summary;
  final List<String> traits;
  final List<String> prevention;

  factory DiseaseGuide.fromMap(Map<String, dynamic> map) {
    return DiseaseGuide(
      name: map["name"] as String? ?? "",
      agentType: map["agent_type"] as String? ?? "",
      agent: map["agent"] as String? ?? "",
      summary: map["summary"] as String? ?? "",
      traits: (map["traits"] as List?)?.cast<String>() ?? [],
      prevention: (map["prevention"] as List?)?.cast<String>() ?? [],
    );
  }
}

class GuideService {
  Map<String, DiseaseGuide>? _en;
  Map<String, DiseaseGuide>? _ha;

  Future<void> load() async {
    _en ??= await _loadFile("assets/guides/disease_guide_en.json");
    _ha ??= await _loadFile("assets/guides/disease_guide_ha.json");
  }

  Future<Map<String, DiseaseGuide>> _loadFile(String asset) async {
    final raw = await rootBundle.loadString(asset);
    final map = jsonDecode(raw) as Map<String, dynamic>;
    return map.map(
      (key, value) => MapEntry(
        key,
        DiseaseGuide.fromMap(value as Map<String, dynamic>),
      ),
    );
  }

  DiseaseGuide guideFor(String classKey, {String lang = "en"}) {
    final table = lang == "ha" ? _ha : _en;
    final hit = table?[classKey];
    if (hit != null) {
      return hit;
    }
    return DiseaseGuide(
      name: classKey.replaceAll("_", " "),
      agentType: "Unknown",
      agent: "",
      summary: "No local advisory text is stored for this class.",
      traits: const [],
      prevention: const [],
    );
  }
}
