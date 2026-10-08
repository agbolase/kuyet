import "dart:io";

import "package:flutter/material.dart";

import "../services/history_service.dart";
import "../theme/tomato_theme.dart";

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key, required this.history});

  final HistoryService history;

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  List<ScanHistoryEntry> _entries = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _reload();
  }

  Future<void> _reload() async {
    final entries = await widget.history.load();
    if (!mounted) {
      return;
    }
    setState(() {
      _entries = entries;
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: RefreshIndicator(
        onRefresh: _reload,
        child: _loading
            ? const Center(child: CircularProgressIndicator())
            : _entries.isEmpty
                ? ListView(
                    children: const [
                      SizedBox(height: 120),
                      Center(
                        child: Text(
                          "No scans yet.\nUse Scan to analyze a leaf.",
                          textAlign: TextAlign.center,
                          style: TextStyle(color: TomatoTheme.muted),
                        ),
                      ),
                    ],
                  )
                : ListView.separated(
                    padding: const EdgeInsets.all(16),
                    itemCount: _entries.length,
                    separatorBuilder: (_, _) => const SizedBox(height: 10),
                    itemBuilder: (context, index) {
                      final entry = _entries[index];
                      return _HistoryTile(
                        entry: entry,
                        history: widget.history,
                      );
                    },
                  ),
      ),
    );
  }
}

class _HistoryTile extends StatelessWidget {
  const _HistoryTile({required this.entry, required this.history});

  final ScanHistoryEntry entry;
  final HistoryService history;

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<File?>(
      future: history.thumbFileFor(entry),
      builder: (context, snap) {
        final thumb = snap.data;
        return ListTile(
          tileColor: const Color(0xFF0C1C16),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          leading: thumb != null
              ? ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: Image.file(thumb, width: 48, height: 48, fit: BoxFit.cover),
                )
              : const Icon(Icons.eco_outlined, color: TomatoTheme.green),
          title: Text(
            entry.displayName,
            style: const TextStyle(
              color: TomatoTheme.text,
              fontWeight: FontWeight.w600,
            ),
          ),
          subtitle: Text(
            "${(entry.confidence * 100).toStringAsFixed(1)}% · "
            "${history.formatWhen(entry.at)}",
            style: const TextStyle(color: TomatoTheme.muted, fontSize: 12),
          ),
        );
      },
    );
  }
}
