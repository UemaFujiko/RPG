FALLBACK_EVENTS = [
    {
        "event_title": "会議での責任転嫁",
        "summary": "中核メンバーが、過去に自分も関与した施策の失敗を若手メンバーの判断ミスとして語り始めた。",
        "risk_tags": ["責任転嫁", "信頼低下", "若手萎縮"],
        "npcs": [
            {"name": "K", "role": "中核メンバー", "stance": "表向き協調", "dialogue": "今回は若手の判断が少し甘かっただけです。"},
            {"name": "M", "role": "若手", "stance": "混乱", "dialogue": "自分だけの判断だったか、少し自信がありません。"}
        ],
        "choices": [
            "議事録と決定経緯を確認する",
            "その場で強く追及する",
            "個別面談で複数証言を集める",
            "曖昧なまま会議を終える"
        ],
        "gm_hint": "記録確認と複数視点の回収が有効。公開叱責は副作用が大きい。"
    },
    {
        "event_title": "裏チャットでの分断",
        "summary": "一部メンバーだけの非公式チャットで、別チームへの不信感が広がっている。",
        "risk_tags": ["派閥化", "情報非対称", "心理的安全性低下"],
        "npcs": [
            {"name": "R", "role": "ベテラン", "stance": "仲間集め", "dialogue": "表では言えないけど、あのチームは信用しない方がいい。"},
            {"name": "S", "role": "新任", "stance": "同調圧力", "dialogue": "合わせないと自分が浮きそうで不安です。"}
        ],
        "choices": [
            "情報共有ルールを明文化する",
            "首謀者探しを始める",
            "全員1on1を行う",
            "しばらく静観する"
        ],
        "gm_hint": "ルール明確化と個別ヒアリングが有効。犯人探しは逆効果になりやすい。"
    },
    {
        "event_title": "成果の横取り",
        "summary": "あるメンバーが、他者の提案を自分の成果として上層部へ伝えていたことが示唆された。",
        "risk_tags": ["評価の歪み", "不公平感", "離職リスク"],
        "npcs": [
            {"name": "T", "role": "高業績メンバー", "stance": "印象操作", "dialogue": "最終的に形にしたのは私なので、私の成果でもあります。"},
            {"name": "Y", "role": "提案者", "stance": "消耗", "dialogue": "もう何を言っても無駄な気がします。"}
        ],
        "choices": [
            "成果物の履歴と貢献者を整理する",
            "被害者に我慢を求める",
            "評価ルールを再確認する",
            "高業績なので問題視しない"
        ],
        "gm_hint": "履歴整理と評価基準明確化が重要。短期業績だけで黙認すると長期損失。"
    }
]


FALLBACK_JUDGMENTS = {
    "議事録と決定経緯を確認する": {
        "effects": {"trust": 5, "safety": 3, "performance": -1, "transparency": 6, "attrition_risk": -1, "faction_risk": -1, "misconduct_risk": -2},
        "reason": "記録に立ち返ることで感情論を避け、責任所在を明確にできた。",
        "lesson": "対人操作が疑われる場面では、公開断罪よりも事実確認と記録の整備が有効。",
        "new_flags": {"evidence_collected": True, "victim_protected": False, "leadership_alerted": False}
    },
    "その場で強く追及する": {
        "effects": {"trust": -3, "safety": -7, "performance": 0, "transparency": 2, "attrition_risk": 2, "faction_risk": 3, "misconduct_risk": 0},
        "reason": "問題提起自体はできたが、公開場面での感情的対立により萎縮と防御が強まった。",
        "lesson": "正しい問題意識でも、介入方法を誤ると心理的安全性を損なう。",
        "new_flags": {"evidence_collected": False, "victim_protected": False, "leadership_alerted": False}
    },
    "個別面談で複数証言を集める": {
        "effects": {"trust": 4, "safety": 4, "performance": -1, "transparency": 4, "attrition_risk": -1, "faction_risk": -2, "misconduct_risk": -1},
        "reason": "複数視点を回収したことで、単独証言への依存を避けられた。",
        "lesson": "組織防衛では、1人の印象より複数の観測点を持つことが重要。",
        "new_flags": {"evidence_collected": True, "victim_protected": True, "leadership_alerted": False}
    },
    "曖昧なまま会議を終える": {
        "effects": {"trust": -4, "safety": -3, "performance": 0, "transparency": -5, "attrition_risk": 2, "faction_risk": 1, "misconduct_risk": 2},
        "reason": "曖昧さを放置したため、不信と情報操作余地が残った。",
        "lesson": "問題の未処理は、中立ではなく悪化要因になることがある。",
        "new_flags": {"evidence_collected": False, "victim_protected": False, "leadership_alerted": False}
    },
    "情報共有ルールを明文化する": {
        "effects": {"trust": 3, "safety": 2, "performance": 0, "transparency": 6, "attrition_risk": -1, "faction_risk": -3, "misconduct_risk": -1},
        "reason": "非公式な情報優位を弱め、共通ルールを導入できた。",
        "lesson": "分断は人ではなく仕組みで弱める。",
        "new_flags": {"evidence_collected": False, "victim_protected": False, "leadership_alerted": True}
    },
    "首謀者探しを始める": {
        "effects": {"trust": -4, "safety": -4, "performance": 0, "transparency": -1, "attrition_risk": 1, "faction_risk": 4, "misconduct_risk": 0},
        "reason": "犯人探しが自己防衛と隠蔽を強めた。",
        "lesson": "初動での犯人探しは、しばしば証拠収集よりも先に対立を固定する。",
        "new_flags": {"evidence_collected": False, "victim_protected": False, "leadership_alerted": False}
    },
    "全員1on1を行う": {
        "effects": {"trust": 3, "safety": 5, "performance": -1, "transparency": 2, "attrition_risk": -1, "faction_risk": -2, "misconduct_risk": 0},
        "reason": "声を上げにくいメンバーから情報を回収できた。",
        "lesson": "見えない萎縮は、全体会議より個別対話で観測しやすい。",
        "new_flags": {"evidence_collected": True, "victim_protected": True, "leadership_alerted": False}
    },
    "しばらく静観する": {
        "effects": {"trust": -3, "safety": -2, "performance": 0, "transparency": -3, "attrition_risk": 1, "faction_risk": 2, "misconduct_risk": 1},
        "reason": "事態を固定化させ、非公式ネットワークの影響が残った。",
        "lesson": "静観は、介入コストを先送りしているだけのことがある。",
        "new_flags": {"evidence_collected": False, "victim_protected": False, "leadership_alerted": False}
    },
    "成果物の履歴と貢献者を整理する": {
        "effects": {"trust": 4, "safety": 2, "performance": 0, "transparency": 5, "attrition_risk": -2, "faction_risk": -1, "misconduct_risk": -2},
        "reason": "貢献の可視化により、不公平感を緩和した。",
        "lesson": "評価の歪みには、印象論よりトレーサビリティが有効。",
        "new_flags": {"evidence_collected": True, "victim_protected": True, "leadership_alerted": True}
    },
    "被害者に我慢を求める": {
        "effects": {"trust": -6, "safety": -6, "performance": 1, "transparency": -2, "attrition_risk": 4, "faction_risk": 1, "misconduct_risk": 2},
        "reason": "短期的な表面安定は得たが、被害者の消耗を放置した。",
        "lesson": "沈黙による秩序は、長期的には離職や不信に転化しやすい。",
        "new_flags": {"evidence_collected": False, "victim_protected": False, "leadership_alerted": False}
    },
    "評価ルールを再確認する": {
        "effects": {"trust": 3, "safety": 1, "performance": 0, "transparency": 4, "attrition_risk": -1, "faction_risk": -1, "misconduct_risk": -1},
        "reason": "制度基準へ戻すことで、個人対立化を避けた。",
        "lesson": "高業績者が絡むときほど、制度の一貫性が防波堤になる。",
        "new_flags": {"evidence_collected": False, "victim_protected": False, "leadership_alerted": True}
    },
    "高業績なので問題視しない": {
        "effects": {"trust": -5, "safety": -4, "performance": 2, "transparency": -4, "attrition_risk": 3, "faction_risk": 2, "misconduct_risk": 3},
        "reason": "短期業績を優先した結果、不公平感と模倣誘因が増えた。",
        "lesson": "成果による免責を認めると、組織規範が崩れやすい。",
        "new_flags": {"evidence_collected": False, "victim_protected": False, "leadership_alerted": False}
    }
}
