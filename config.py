WASMACHINE_WORKFLOW = {
    "nodes": [
        {"name": "Sorteren wasmand ouders", "duration": 5, "resources": 1, "cost": 5},
        {"name": "Sorteren wasmand dochter 1", "duration": 1000, "resources": 1000, "cost": 1000},
        {"name": "Sorteren wasmand dochter 2"},
        {
            "name": "Droger nodig?",
            "type": "decision",
            "probabilities": {
                "Ja": 0.6,
                "Nee": 0.4
            }
        },
        {"name": "Sorteren wasmand ouders inc sokken vouwen"},
        {"name": "Sorteren wasmand dochter 1 inc sokken vouwen"},
        {"name": "Sorteren wasmand dochter 2 inc sokken vouwen"},
        {"name": "Beddengoed wassen", "duration": 1000, "resources": 1, "cost": 1000},
        {"name": "Handdoeken wassen"},
        {"name": "Kleding ophangen ouders"},
        {"name": "Kleding ophangen dochter 1", "duration": 1000, "resources": 1, "cost": 1000},
        {"name": "Kleding ophangen dochter 2"},
        {"name": "Wasmachine", "duration": 1000, "resources": 1, "cost": 2000},
        {"name": "Sokken vouwen voor sorteren"},
        {"name": "Sokken vouwen na sorteren"},
        {"name": "Ophangen", "duration": 1000, "resources": 1},
        {"name": "Droger", "duration": 1000, "cost": 2000}
    ],
    "edges": [
        {"from": "Ophangen", "to": "Sorteren wasmand ouders inc sokken vouwen"},
        {"from": "Ophangen", "to": "Sorteren wasmand dochter 1 inc sokken vouwen"},
        {"from": "Ophangen", "to": "Sorteren wasmand dochter 2 inc sokken vouwen"},
        {"from": "Ophangen", "to": "Sokken vouwen voor sorteren"},
        {"from": "Wasmachine", "to": "Droger nodig?"},
        {"from": "Droger nodig?", "to": "Droger", "label": "Ja"},
        {"from": "Droger", "to": "Ophangen", "label": "Ja"},
        {"from": "Droger nodig?", "to": "Ophangen", "label": "Nee"},
        {"from": "Sokken vouwen voor sorteren", "to": "Sorteren wasmand ouders"},   
        {"from": "Sokken vouwen voor sorteren", "to": "Sorteren wasmand dochter 1"},
        {"from": "Sokken vouwen voor sorteren", "to": "Sorteren wasmand dochter 2"},
        {"from": "Sorteren wasmand ouders inc sokken vouwen", "to": "Kleding ophangen ouders"},
        {"from": "Sorteren wasmand dochter 1 inc sokken vouwen", "to": "Kleding ophangen dochter 1"},
        {"from": "Sorteren wasmand dochter 2 inc sokken vouwen", "to": "Kleding ophangen dochter 2"},
        {"from": "Sorteren wasmand ouders", "to": "Kleding ophangen ouders"},
        {"from": "Sorteren wasmand dochter 1", "to": "Kleding ophangen dochter 1"},
        {"from": "Sorteren wasmand dochter 2", "to": "Kleding ophangen dochter 2"},
        {"from": "Beddengoed wassen", "to": "Kleding ophangen ouders"},
        {"from": "Handdoeken wassen", "to": "Kleding ophangen ouders"},
    ]
}