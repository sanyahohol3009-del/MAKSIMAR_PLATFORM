from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_first_real_picture_contract import (
    build_operator_dashboard_first_real_picture_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_render_result_contract import (
    build_visual_hud_render_result_contract,
)


@dataclass(frozen=True, slots=True)
class OperatorDashboardFirstRenderArtifact:
    """Visible HTML artifact for the first truthful live operator screen."""

    artifact_id: str
    dashboard_id: str
    workspace_id: str
    output_path: str
    title: str
    html: str


def _severity_color(severity: str) -> str:
    """Resolve severity color token for HTML rendering."""
    if severity == "critical":
        return "#ff5f56"
    if severity == "warning":
        return "#ffbd2e"
    return "#27c93f"


def _build_core_ring_svg() -> str:
    """Build minimal SVG for core/rings composition."""
    return """
<svg viewBox="0 0 600 420" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" aria-label="Operator core topology">
  <defs>
    <radialGradient id="coreGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#5ee7ff" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#5ee7ff" stop-opacity="0.05"/>
    </radialGradient>
  </defs>

  <circle cx="300" cy="210" r="62" fill="url(#coreGlow)" stroke="#5ee7ff" stroke-width="2"/>
  <circle cx="300" cy="210" r="110" fill="none" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="6 6"/>
  <circle cx="300" cy="210" r="160" fill="none" stroke="#22c55e" stroke-width="1.5" stroke-dasharray="10 8"/>

  <text x="300" y="200" text-anchor="middle" fill="#e5f4ff" font-size="24" font-family="Arial">ЯДРО</text>
  <text x="300" y="224" text-anchor="middle" fill="#93c5fd" font-size="12" font-family="Arial">truth-bound operator core</text>

  <circle cx="300" cy="50" r="10" fill="#3b82f6"/>
  <text x="300" y="32" text-anchor="middle" fill="#93c5fd" font-size="11" font-family="Arial">СТАТУС</text>

  <circle cx="462" cy="210" r="10" fill="#22c55e"/>
  <text x="520" y="214" text-anchor="middle" fill="#86efac" font-size="11" font-family="Arial">ОБЪЯСНИТЕ</text>

  <circle cx="300" cy="370" r="10" fill="#f59e0b"/>
  <text x="300" y="395" text-anchor="middle" fill="#fcd34d" font-size="11" font-family="Arial">ТИКЕР</text>

  <circle cx="138" cy="210" r="10" fill="#8b5cf6"/>
  <text x="92" y="214" text-anchor="middle" fill="#c4b5fd" font-size="11" font-family="Arial">NAV</text>

  <line x1="300" y1="60" x2="300" y2="148" stroke="#60a5fa" stroke-width="1.5"/>
  <line x1="452" y1="210" x2="370" y2="210" stroke="#4ade80" stroke-width="1.5"/>
  <line x1="300" y1="360" x2="300" y2="272" stroke="#fbbf24" stroke-width="1.5"/>
  <line x1="148" y1="210" x2="230" y2="210" stroke="#a78bfa" stroke-width="1.5"/>
</svg>
""".strip()


def build_operator_dashboard_first_render_artifact() -> OperatorDashboardFirstRenderArtifact:
    """Build visible HTML artifact from truthful operator payload."""
    first_real_picture_contract = build_operator_dashboard_first_real_picture_contract()
    render_result_contract = build_visual_hud_render_result_contract()

    first_real_picture_entry = first_real_picture_contract.entries[0]
    render_result_entry = render_result_contract.entries[0]

    status_color = _severity_color(first_real_picture_entry.status_bar_severity)
    ticker_color = _severity_color(first_real_picture_entry.ticker_severity)

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <title>Операторский экран MAKSIMAR</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta http-equiv="refresh" content="5" />
  <style>
    :root {{
      --bg: #07111d;
      --panel: rgba(15, 27, 43, 0.96);
      --panel-2: rgba(19, 35, 56, 0.96);
      --text: #e6f0ff;
      --muted: #8ea3bf;
      --line: #28435f;
      --shadow: 0 12px 30px rgba(0, 0, 0, 0.24);
      --gap: 12px;
      --radius: 18px;
    }}

    * {{
      box-sizing: border-box;
      min-width: 0;
    }}

    html, body {{
      margin: 0;
      padding: 0;
      min-height: 100%;
      background: linear-gradient(180deg, #040b14 0%, #081220 100%);
      color: var(--text);
      font-family: Arial, Helvetica, sans-serif;
      overflow-x: hidden;
    }}

    body {{
      min-height: 100vh;
    }}

    .shell {{
      min-height: 100vh;
      display: grid;
      grid-template-columns: minmax(220px, 260px) minmax(0, 1fr) minmax(260px, 320px);
      grid-template-rows: auto 1fr auto;
      grid-template-areas:
        "top top top"
        "left center right"
        "bottom bottom bottom";
      gap: var(--gap);
      padding: var(--gap);
      align-items: stretch;
    }}

    .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow: hidden;
    }}

    .top {{
      grid-area: top;
      display: grid;
      grid-template-columns: repeat(4, minmax(180px, 1fr));
      gap: 10px;
      padding: 10px;
      align-items: stretch;
    }}

    .left {{
      grid-area: left;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .center {{
      grid-area: center;
      padding: 14px;
      display: grid;
      grid-template-rows: auto minmax(420px, 1fr) auto;
      gap: 14px;
      align-items: stretch;
    }}

    .right {{
      grid-area: right;
      padding: 14px;
      display: grid;
      grid-template-rows: auto auto 1fr;
      gap: 12px;
      align-items: stretch;
    }}

    .bottom {{
      grid-area: bottom;
      padding: 12px 14px;
      display: grid;
      grid-template-columns: 1.2fr 1fr 1fr;
      gap: 12px;
      align-items: stretch;
    }}

    .headline {{
      font-size: 12px;
      letter-spacing: 0.12em;
      color: var(--muted);
      text-transform: uppercase;
      margin-bottom: 8px;
      white-space: normal;
      word-break: break-word;
    }}

    .value {{
      font-size: clamp(18px, 2vw, 30px);
      font-weight: 700;
      line-height: 1.15;
      white-space: normal;
      word-break: break-word;
      overflow-wrap: anywhere;
    }}

    .sub {{
      font-size: 13px;
      color: var(--muted);
      margin-top: 6px;
      line-height: 1.45;
      white-space: normal;
      word-break: break-word;
      overflow-wrap: anywhere;
    }}

    .nav-list {{
      display: grid;
      gap: 8px;
      margin-top: 4px;
    }}

    .nav-item {{
      padding: 10px 12px;
      border-radius: 12px;
      border: 1px solid var(--line);
      background: var(--panel-2);
      font-size: 14px;
      white-space: normal;
      word-break: break-word;
    }}

    .center-top {{
      display: grid;
      grid-template-columns: repeat(4, minmax(140px, 1fr));
      gap: 10px;
    }}

    .mini {{
      padding: 12px;
      border-radius: 14px;
      border: 1px solid var(--line);
      background: var(--panel-2);
      min-width: 0;
    }}

    .core-box {{
      min-height: 420px;
      border-radius: 18px;
      border: 1px solid var(--line);
      background:
        radial-gradient(circle at center, rgba(94, 231, 255, 0.08), transparent 45%),
        linear-gradient(180deg, rgba(19, 35, 56, 0.95), rgba(10, 20, 34, 0.95));
      padding: 16px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}

    .core-svg-wrap {{
      flex: 1 1 auto;
      min-height: 320px;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }}

    .core-svg-wrap svg {{
      width: 100%;
      height: auto;
      max-height: min(58vh, 620px);
      display: block;
    }}

    .right-block {{
      padding: 12px;
      border-radius: 14px;
      border: 1px solid var(--line);
      background: var(--panel-2);
      min-width: 0;
    }}

    .severity-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 10px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.02);
      font-size: 13px;
      margin-top: 8px;
      white-space: normal;
      flex-wrap: wrap;
    }}

    .dot {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
      display: inline-block;
      flex: 0 0 auto;
    }}

    .kv {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 8px;
      font-size: 14px;
      padding: 6px 0;
      border-bottom: 1px solid rgba(255,255,255,0.05);
      align-items: start;
    }}

    .kv:last-child {{
      border-bottom: 0;
    }}

    .mono {{
      font-family: "Courier New", Courier, monospace;
      font-size: 12px;
      color: #c5d8f3;
      line-height: 1.5;
      white-space: pre-wrap;
      word-break: break-word;
      overflow-wrap: anywhere;
    }}

    .compact-block {{
      min-height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
    }}

    @media (max-width: 1600px) {{
      .shell {{
        grid-template-columns: 220px minmax(0, 1fr) 280px;
      }}
    }}

    @media (max-width: 1320px) {{
      .shell {{
        grid-template-columns: 240px minmax(0, 1fr);
        grid-template-areas:
          "top top"
          "left center"
          "right right"
          "bottom bottom";
      }}

      .right {{
        grid-template-columns: repeat(3, minmax(0, 1fr));
        grid-template-rows: none;
      }}

      .center {{
        grid-template-rows: auto minmax(360px, 1fr) auto;
      }}
    }}

    @media (max-width: 980px) {{
      .shell {{
        grid-template-columns: 1fr;
        grid-template-areas:
          "top"
          "left"
          "center"
          "right"
          "bottom";
      }}

      .top {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}

      .center-top {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}

      .right {{
        grid-template-columns: 1fr;
      }}

      .bottom {{
        grid-template-columns: 1fr;
      }}

      .center {{
        grid-template-rows: auto minmax(320px, 1fr) auto;
      }}
    }}

    @media (max-width: 640px) {{
      .shell {{
        padding: 8px;
        gap: 8px;
      }}

      .top {{
        grid-template-columns: 1fr;
      }}

      .center-top {{
        grid-template-columns: 1fr;
      }}

      .left, .center, .right, .bottom {{
        padding: 10px;
      }}

      .core-box {{
        min-height: 300px;
      }}

      .core-svg-wrap {{
        min-height: 240px;
      }}
    }}

    @media (orientation: portrait) and (min-width: 700px) {{
      .shell {{
        grid-template-columns: 1fr;
        grid-template-areas:
          "top"
          "center"
          "left"
          "right"
          "bottom";
      }}

      .top {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}

      .center-top {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}

      .right {{
        grid-template-columns: 1fr;
      }}

      .bottom {{
        grid-template-columns: 1fr;
      }}

      .center {{
        grid-template-rows: auto minmax(460px, 1fr) auto;
      }}

      .core-svg-wrap svg {{
        max-height: 52vh;
      }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <div class="card top">
      <div class="card" style="padding:12px;">
        <div class="headline">Системное здоровье</div>
        <div class="value">Статус: {escape(first_real_picture_entry.status_bar_severity).upper()}</div>
        <div class="severity-pill">
          <span class="dot" style="background:{status_color};"></span>
          truthful runtime state
        </div>
        <div class="sub">{escape(render_result_entry.top_summary)}</div>
      </div>

      <div class="card" style="padding:12px;">
        <div class="headline">Роль в показе</div>
        <div class="value">Первичный оператор</div>
        <div class="sub">surface={escape(first_real_picture_entry.renderer_surface_id)}</div>
      </div>

      <div class="card" style="padding:12px;">
        <div class="headline">Режим сцены</div>
        <div class="value">{escape(render_result_entry.scene_mode)}</div>
        <div class="sub">screen={escape(first_real_picture_entry.screen_id)}</div>
      </div>

      <div class="card" style="padding:12px;">
        <div class="headline">Слои</div>
        <div class="value">{first_real_picture_entry.visible_layers}/{first_real_picture_entry.total_layers}</div>
        <div class="sub">render_state={escape(render_result_entry.render_state)}</div>
      </div>
    </div>

    <div class="card left">
      <div class="headline">Боковая панель</div>
      <div class="nav-list">
        <div class="nav-item">Мониторинг</div>
        <div class="nav-item">Проекты</div>
        <div class="nav-item">Память</div>
        <div class="nav-item">Симуляция</div>
        <div class="nav-item">Физика</div>
        <div class="nav-item">Голос</div>
        <div class="nav-item">Сервисы ИИ</div>
        <div class="nav-item">Места действия</div>
      </div>
      <div class="sub" style="margin-top:14px;">
        workspace={escape(first_real_picture_entry.workspace_id)}<br/>
        dashboard={escape(first_real_picture_entry.dashboard_id)}
      </div>
    </div>

    <div class="card center">
      <div class="center-top">
        <div class="mini">
          <div class="headline">Топология</div>
          <div class="value">{first_real_picture_entry.topology_overlay_entries}</div>
          <div class="sub">оверлейные записи</div>
        </div>
        <div class="mini">
          <div class="headline">Сигналы</div>
          <div class="value">{first_real_picture_entry.signal_overlay_entries}</div>
          <div class="sub">оверлейные записи</div>
        </div>
        <div class="mini">
          <div class="headline">Объяснимость</div>
          <div class="value">{first_real_picture_entry.explainability_entries}</div>
          <div class="sub">записи в боковой панели</div>
        </div>
        <div class="mini">
          <div class="headline">Тикер</div>
          <div class="value">{escape(first_real_picture_entry.ticker_severity).upper()}</div>
          <div class="sub">состояние логарифмичного потока</div>
        </div>
      </div>

      <div class="core-box">
        <div class="headline">Основное рабочее пространство / ядро оператора</div>
        <div class="core-svg-wrap">
          {_build_core_ring_svg()}
        </div>
      </div>

      <div class="mini">
        <div class="headline">Центральное резюме</div>
        <div class="mono">{escape(render_result_entry.center_summary)}</div>
      </div>
    </div>

    <div class="card right">
      <div class="right-block compact-block">
        <div class="headline">Панель объяснения</div>
        <div class="mono">{escape(render_result_entry.right_summary)}</div>
      </div>

      <div class="right-block compact-block">
        <div class="headline">Топ-аннотация</div>
        <div class="mono">{escape(render_result_entry.top_summary)}</div>
      </div>

      <div class="right-block compact-block">
        <div class="headline">Почему именно такое состояние</div>
        <div class="kv"><span>Степень тяжести статуса</span><span>{escape(first_real_picture_entry.status_bar_severity)}</span></div>
        <div class="kv"><span>Тяжесть тикера</span><span>{escape(first_real_picture_entry.ticker_severity)}</span></div>
        <div class="kv"><span>Поверхность рендера</span><span>{escape(first_real_picture_entry.renderer_surface_id)}</span></div>
        <div class="kv"><span>Тема</span><span>{escape(first_real_picture_entry.theme_id)}</span></div>
        <div class="kv"><span>Экран</span><span>{escape(first_real_picture_entry.screen_id)}</span></div>
      </div>
    </div>

    <div class="card bottom">
      <div>
        <div class="headline">Командная полоса</div>
        <div class="mono">Открыть мониторинг · Открытая диагностика · Объяснить текущее состояние · Маршрутизация шоу · Показать активные оповещения</div>
      </div>
      <div>
        <div class="headline">Нижняя сводка</div>
        <div class="mono">{escape(render_result_entry.bottom_summary)}</div>
      </div>
      <div>
        <div class="headline">Артефакт</div>
        <div class="mono">первый правдивый экран живого оператора (HTML-артефакт)</div>
      </div>
    </div>
  </div>
</body>
</html>
""".strip()

    return OperatorDashboardFirstRenderArtifact(
        artifact_id="operator_dashboard_first_render_artifact_001",
        dashboard_id=first_real_picture_entry.dashboard_id,
        workspace_id=first_real_picture_entry.workspace_id,
        output_path="SANDBOX/operator_dashboard_first_render_artifact.html",
        title="Операторский экран MAKSIMAR",
        html=html,
    )


def write_operator_dashboard_first_render_artifact(
    output_path: str | Path,
) -> Path:
    """Write the first visible operator screen HTML artifact to disk."""
    artifact = build_operator_dashboard_first_render_artifact()
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(artifact.html, encoding="utf-8")
    return path
