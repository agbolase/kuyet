"""Scan history page UI."""

from __future__ import annotations

import base64
from datetime import datetime

import streamlit as st

import config
import scan_history
from ui_theme import inject_css


def _format_when(iso_ts: str) -> str:
    try:
        when = datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
        return when.strftime("%d %b %Y, %H:%M UTC")
    except ValueError:
        return iso_ts


def _confidence_badge(confidence: float, low: bool) -> str:
    pct = confidence * 100
    level = "low" if low else ("mid" if pct < 80 else "high")
    return f'<span class="tc-conf tc-conf-{level}">{pct:.1f}%</span>'


HISTORY_CSS = """
.tc-history-header { margin: 0.5rem 0 1.5rem; }
.tc-history-header h1 {
  font-size: 1.85rem;
  margin: 0 0 0.35rem;
  letter-spacing: -0.02em;
}
.tc-history-header p { color: var(--tc-muted); margin: 0; }
.tc-stat-row {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.tc-stat {
  background: var(--tc-panel-bg);
  border: 1px solid var(--tc-panel-border);
  border-radius: 0.85rem;
  padding: 1rem 1.15rem;
}
.tc-stat-label {
  color: var(--tc-muted);
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 0.35rem;
}
.tc-stat-value {
  font-size: 1.45rem;
  font-weight: 700;
  color: var(--tc-text);
}
.tc-log-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 0.55rem;
}
.tc-log-table th {
  text-align: left;
  color: var(--tc-muted);
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0 0.75rem 0.35rem;
}
.tc-log-row td {
  background: var(--tc-panel-bg);
  border-top: 1px solid var(--tc-panel-border);
  border-bottom: 1px solid var(--tc-panel-border);
  padding: 0.75rem;
  vertical-align: middle;
}
.tc-log-row td:first-child {
  border-left: 1px solid var(--tc-panel-border);
  border-radius: 0.75rem 0 0 0.75rem;
  width: 72px;
}
.tc-log-row td:last-child {
  border-right: 1px solid var(--tc-panel-border);
  border-radius: 0 0.75rem 0.75rem 0;
}
.tc-log-thumb {
  width: 56px;
  height: 56px;
  object-fit: cover;
  border-radius: 0.55rem;
  border: 1px solid var(--tc-panel-border);
}
.tc-log-title { font-weight: 600; color: var(--tc-text); }
.tc-log-sub { color: var(--tc-muted); font-size: 0.86rem; margin-top: 0.15rem; }
.tc-conf {
  display: inline-block;
  padding: 0.25rem 0.55rem;
  border-radius: 999px;
  font-size: 0.82rem;
  font-weight: 600;
}
.tc-conf-high { background: rgba(61, 220, 132, 0.18); color: var(--tc-green); }
.tc-conf-mid { background: rgba(255, 193, 7, 0.16); color: #d4a017; }
.tc-conf-low { background: rgba(224, 107, 90, 0.18); color: var(--tc-tomato); }
.tc-empty {
  text-align: center;
  padding: 2.5rem 1rem;
  border: 1px dashed var(--tc-panel-border);
  border-radius: 1rem;
  background: var(--tc-panel-bg);
}
.tc-empty h3 { margin: 0 0 0.5rem; }
.tc-empty p { color: var(--tc-muted); margin: 0 0 1rem; }
.tc-table-scroll {
  width: 100%;
  max-width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
@media (max-width: 900px) {
  .tc-stat-row { grid-template-columns: 1fr; }
  .tc-log-table thead { display: none; }
  .tc-log-row, .tc-log-row td { display: block; width: 100%; border-radius: 0.75rem !important; }
  .tc-log-row { margin-bottom: 0.75rem; }
}
@media (max-width: 768px) {
  .tc-history-header h1 { font-size: 1.45rem; }
  .tc-history-header p { font-size: 0.88rem; }
  .tc-stat-value { font-size: 1.2rem; }
  .tc-log-title { font-size: 0.95rem; }
  .tc-log-sub { font-size: 0.8rem; }
  .tc-table-scroll {
    margin-left: calc(-1 * max(0.65rem, env(safe-area-inset-left)));
    margin-right: calc(-1 * max(0.65rem, env(safe-area-inset-right)));
    padding-left: max(0.65rem, env(safe-area-inset-left));
    padding-right: max(0.65rem, env(safe-area-inset-right));
  }
}
"""


def render_history_page() -> None:
    inject_css(HISTORY_CSS)
    st.markdown('<div class="tc-page-content">', unsafe_allow_html=True)
    entries = scan_history.load_entries()

    st.markdown(
        """
        <div class="tc-history-header">
          <h1>Scan history</h1>
          <p>All completed leaf scans are listed below, newest first.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    total = len(entries)
    if total == 0:
        st.markdown(
            """
            <div class="tc-empty">
              <h3>No scans yet</h3>
              <p>Run your first leaf scan and the result will appear here automatically.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("📷 Scan a leaf", type="primary", key="history_empty_scan"):
            st.switch_page("pages/Scan.py")
        return

    latest = _format_when(entries[0]["at"])
    low_count = sum(1 for item in entries if item.get("low_confidence"))
    healthy = sum(1 for item in entries if item.get("predicted_key") == "Tomato_healthy")

    st.markdown(
        f"""
        <div class="tc-stat-row">
          <div class="tc-stat">
            <div class="tc-stat-label">Total scans</div>
            <div class="tc-stat-value">{total}</div>
          </div>
          <div class="tc-stat">
            <div class="tc-stat-label">Latest scan</div>
            <div class="tc-stat-value" style="font-size:1rem;">{latest}</div>
          </div>
          <div class="tc-stat">
            <div class="tc-stat-label">Healthy reads</div>
            <div class="tc-stat-value">{healthy}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if low_count:
        st.caption(f"{low_count} scan(s) were flagged as low confidence (below {config.CONFIDENCE_WARN_THRESHOLD:.0%}).")

    rows = ['<table class="tc-log-table"><thead><tr>']
    rows.append(
        "<th>Preview</th><th>Result</th><th>Confidence</th><th>Top matches</th><th>When</th></tr></thead><tbody>"
    )
    for entry in entries:
        thumb_file = scan_history.thumb_path(entry.get("thumb", ""))
        if thumb_file.is_file():
            encoded = base64.b64encode(thumb_file.read_bytes()).decode("ascii")
            thumb_html = f'<img class="tc-log-thumb" src="data:image/jpeg;base64,{encoded}" alt="Leaf preview" />'
        else:
            thumb_html = '<div class="tc-log-thumb"></div>'

        top3 = entry.get("top3") or []
        top_text = "<br/>".join(
            f"{idx + 1}. {item.get('label', item.get('key', ''))} ({item.get('score', 0) * 100:.1f}%)"
            for idx, item in enumerate(top3)
        )
        source = entry.get("source_name") or "Uploaded image"
        tta = "Multi-region" if entry.get("use_tta") else "Single region"
        lang = (entry.get("lang") or "en").upper()
        sub = f"{source} · {tta} · {lang}"

        rows.append('<tr class="tc-log-row">')
        rows.append(f"<td>{thumb_html}</td>")
        rows.append(
            f'<td><div class="tc-log-title">{entry.get("label", "Unknown")}</div>'
            f'<div class="tc-log-sub">{sub}</div></td>'
        )
        rows.append(
            f"<td>{_confidence_badge(entry.get('confidence', 0), entry.get('low_confidence', False))}</td>"
        )
        rows.append(f'<td><span class="tc-log-sub">{top_text}</span></td>')
        rows.append(f'<td><span class="tc-log-sub">{_format_when(entry.get("at", ""))}</span></td>')
        rows.append("</tr>")
    rows.append("</tbody></table>")
    st.markdown(f'<div class="tc-table-scroll">{"".join(rows)}</div>', unsafe_allow_html=True)

    with st.expander("Manage history"):
        st.caption("Clearing removes all saved scan logs and thumbnails from this device.")
        if st.button("Clear all scan history", type="secondary", key="clear_scan_history"):
            scan_history.clear_history()
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
