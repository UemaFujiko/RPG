from __future__ import annotations

import pandas as pd
import streamlit as st

from src.ai_client import is_ai_enabled, get_model_name
from src.event_generator import generate_event
from src.game_state import init_state, get_game, reset_state, apply_judgment, final_rank
from src.judge_engine import judge_choice

st.set_page_config(page_title="Team Guardian RPG", page_icon="🛡️", layout="wide")
init_state()
game = get_game()


def sidebar_controls():
    with st.sidebar:
        st.title("🛡️ Team Guardian RPG")
        st.caption("有害行動からチームを守る防衛型RPG")
        st.divider()
        st.write(f"AIモード: {'ON' if is_ai_enabled() else 'OFF'}")
        if is_ai_enabled():
            st.caption(f"Model: {get_model_name()}")

        game["difficulty"] = st.selectbox(
            "難易度",
            ["易しい", "標準", "難しい"],
            index=["易しい", "標準", "難しい"].index(game["difficulty"]),
        )
        game["team_type"] = st.selectbox(
            "チームタイプ",
            ["コンサル会社", "学校組織", "病院", "スタートアップ", "行政組織"],
            index=["コンサル会社", "学校組織", "病院", "スタートアップ", "行政組織"].index(game["team_type"]),
        )
        if st.button("ゲームをリセット", use_container_width=True):
            reset_state()
            st.rerun()

        st.divider()
        st.metric("Turn", f"{game['turn']} / {game['max_turns']}")
        st.metric("信頼", game["trust"])
        st.metric("心理的安全性", game["safety"])
        st.metric("業績", game["performance"])
        st.metric("透明性", game["transparency"])
        st.metric("離職リスク", game["attrition_risk"])
        st.metric("派閥化リスク", game["faction_risk"])
        st.metric("不正リスク", game["misconduct_risk"])


def render_home():
    st.title("🛡️ Team Guardian RPG")
    st.subheader("操作・分断・責任転嫁から、あなたのチームを守る")
    st.write(
        "このゲームは、架空のチームに起きる有害行動への対応を学ぶ教育用シミュレーターです。"
        " 実在人物の診断ではなく、行動パターンと組織防衛の訓練を目的としています。"
    )
    col1, col2 = st.columns(2)
    with col1:
        st.info(
            "**プレイヤーの役割**\n"
            "- マネージャー\n"
            "- PM\n"
            "- HR\n"
            "- 現場リーダー"
        )
    with col2:
        st.warning(
            "**勝利条件の目安**\n"
            "- 信頼と心理的安全性を維持\n"
            "- 業績と透明性を確保\n"
            "- 離職・派閥化・不正リスクを抑制"
        )
    st.success("左のサイドバーで難易度やチームタイプを設定し、[プレイ] タブへ進んでください。")


def render_play():
    st.header("🎮 プレイ")
    if game["game_over"]:
        st.error("ゲームは終了しています。左のサイドバーからリセットしてください。")
        st.subheader("最終評価")
        st.write(final_rank())
        return

    if game["current_event"] is None:
        event = generate_event(game)
        game["current_event"] = event.model_dump()
    else:
        from src.data_models import EventPayload
        event = EventPayload(**game["current_event"])

    st.subheader(f"Turn {game['turn']}: {event.event_title}")
    st.write(event.summary)

    tags = " / ".join(event.risk_tags) if event.risk_tags else "なし"
    st.caption(f"リスクタグ: {tags}")

    with st.expander("NPCの様子"):
        for npc in event.npcs:
            st.markdown(f"**{npc.name}**（{npc.role} / {npc.stance}）")
            if npc.dialogue:
                st.write(f"「{npc.dialogue}」")

    st.markdown("### 対応を選んでください")
    for idx, choice in enumerate(event.choices, start=1):
        if st.button(f"{idx}. {choice}", key=f"choice_{game['turn']}_{idx}", use_container_width=True):
            result = judge_choice(game, event, choice)
            apply_judgment(result.model_dump(), choice)
            st.session_state["last_result"] = result.model_dump()
            st.rerun()

    if "last_result" in st.session_state:
        st.divider()
        st.markdown("### 直前ターンの判定")
        st.write(st.session_state["last_result"]["reason"])
        st.info(st.session_state["last_result"]["lesson"])


def render_status():
    st.header("📊 チーム状態")
    metrics = pd.DataFrame(
        {
            "指標": ["信頼", "心理的安全性", "業績", "透明性", "離職リスク", "派閥化リスク", "不正リスク"],
            "値": [
                game["trust"],
                game["safety"],
                game["performance"],
                game["transparency"],
                game["attrition_risk"],
                game["faction_risk"],
                game["misconduct_risk"],
            ],
        }
    )
    st.bar_chart(metrics.set_index("指標"))

    st.subheader("フラグ")
    st.json(game["flags"])

    st.subheader("行動ログ")
    if game["history"]:
        st.dataframe(pd.DataFrame(game["history"]), use_container_width=True)
    else:
        st.write("まだログはありません。")

    if game["game_over"]:
        st.success(f"最終評価: {final_rank()}")


def render_learning():
    st.header("📘 学習モード")
    st.markdown(
        """
### このゲームで学ぶこと
- **事実確認の重要性**: 記録、議事録、成果物履歴は防衛の基礎です。
- **犯人探しより構造是正**: 問題を個人攻撃だけで捉えると、組織がさらに壊れやすくなります。
- **心理的安全性と透明性**: 声を上げやすい場と、情報共有の仕組みは分断対策に有効です。
- **高業績者の例外化を避ける**: 短期成果を理由に規範逸脱を免責すると、長期的損失が大きくなります。

### 発展案
- チームタイプごとのイベント差分
- 証拠ポイント、被害者保護ポイントなどの隠し変数
- レポート出力機能
- イベントCSV蓄積と分析
        """
    )


def render_settings():
    st.header("⚙️ 設定")
    st.write("アプリは、APIキーなしでも固定イベントで動作します。")
    st.code(
        "OPENAI_API_KEY=your_api_key_here\nOPENAI_MODEL=gpt-4.1-mini\nUSE_AI=true",
        language="bash",
    )
    st.write("`.env` をプロジェクト直下に置くと、AI生成モードを利用できます。")
    st.write(f"現在のAI利用状態: {'有効' if is_ai_enabled() else '無効'}")
    if is_ai_enabled():
        st.write(f"現在のモデル: {get_model_name()}")


sidebar_controls()

pages = {
    "ホーム": render_home,
    "プレイ": render_play,
    "状態": render_status,
    "学習": render_learning,
    "設定": render_settings,
}

selected = st.radio("ページ", list(pages.keys()), horizontal=True, label_visibility="collapsed")
pages[selected]()
