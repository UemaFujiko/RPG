# Team Guardian RPG

架空のチーム内で発生する「操作・分断・責任転嫁・情報隠し」などの有害行動から、
チームを守るための防衛型マネジメントRPGです。

## 特徴
- Streamlitで動く対話型アプリ
- APIキーがなくても固定イベントでプレイ可能
- OpenAI APIを設定すると、イベント・NPC会話・判定をAI生成に切替可能
- 実在人物の診断ではなく、架空の行動パターンを対象化
- 学習用の解説モード付き

## 1. セットアップ

### Windows PowerShell
```powershell
cd team_guardian_rpg
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

`.env` の `OPENAI_API_KEY` を設定してください。

## 2. 起動
```powershell
streamlit run app.py
```

## 3. 画面構成
- ホーム: ゲーム説明と開始
- プレイ: ターン進行、イベント対応
- 状態: チーム状態と履歴
- 学習: 組織防衛の考え方
- 設定: AI利用や難易度の確認

## 4. APIなしでの動作
`.env` を作らなくても固定イベントでプレイできます。

## 5. APIありでの動作
- `OPENAI_API_KEY` を設定
- `USE_AI=true`
- `OPENAI_MODEL` は Responses API に対応したモデル名を設定

## 6. 注意
このアプリは教育・訓練・組織マネジメント学習用です。
実在人物の精神医学的診断や人格断定に使わないでください。
