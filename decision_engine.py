import random

def evaluate_rule(rule, context):
    try:
        return eval(rule, {}, context)
    except:
        return False


def decide(node, context):
    """
    node = decision node config
    context = data van case (bijv humidity, urgency)
    """

    # RULE-BASED
    if node.get("model") == "simple_rule":
        rules = node.get("rules", {})

        for rule, outcome in rules.items():
            if rule == "else":
                continue
            if evaluate_rule(rule, context):
                return outcome

        return rules.get("else")

    # PROBABILISTIC fallback
    if node.get("probabilities"):
        probs = node["probabilities"]
        return random.choices(list(probs.keys()), weights=probs.values())[0]

    return None