from .KnowledgePicker import KnowledgePicker

class InferenceEngine:
    def __init__(self):
        self.kb = KnowledgePicker()

    def evaluate_condition(self, condition, facts_with_weights):
        cond_type = condition.get("type", "AND")
        items = condition["items"]

        if cond_type == "AND":
            for item in items:
                fact = item["fact"]
                required_weight = item.get("weight", 1.0)
                if fact not in facts_with_weights or facts_with_weights[fact] < required_weight:
                    return False, 0
            total_weight = sum(facts_with_weights[item["fact"]] for item in items if item["fact"] in facts_with_weights)
            avg_weight = total_weight / len(items)
            return True, avg_weight

        elif cond_type == "OR":
            for item in items:
                fact = item["fact"]
                required_weight = item.get("weight", 1.0)
                if fact in facts_with_weights and facts_with_weights[fact] >= required_weight:
                    return True, facts_with_weights[fact]
            return False, 0

        elif cond_type == "NOT":
            for item in items:
                fact = item["fact"]
                if fact in facts_with_weights:
                    return False, 0
            return True, 1.0

        return False, 0

    def forward_chain(self, initial_facts_with_weights):
        facts_with_weights = initial_facts_with_weights.copy()
        explanations = []
        changed = True

        while changed:
            changed = False
            applicable_rules = []

            for rule in self.kb.get_all_rules():
                is_satisfied, condition_weight = self.evaluate_condition(rule.conditions, facts_with_weights)
                conclusion_fact = rule.conclusion["fact"]
                conclusion_weight = rule.conclusion["weight"]
                priority = rule.priority

                if is_satisfied and conclusion_fact not in facts_with_weights:
                    applicable_rules.append((priority, condition_weight, rule))
                    print(applicable_rules)

            if applicable_rules:
                applicable_rules.sort(key=lambda x: x[0], reverse=True)
                _, _, selected_rule = applicable_rules[0]

                conclusion_fact = selected_rule.conclusion["fact"]
                conclusion_weight = selected_rule.conclusion["weight"]
                facts_with_weights[conclusion_fact] = conclusion_weight

                conclusion_obj = self.kb.get_conclusion_by_code(conclusion_fact)
                name = conclusion_obj.name if conclusion_obj else conclusion_fact

                explanations.append(
                    f"Aturan {selected_rule.rule_id}: {selected_rule.description} => {name} (Bobot: {conclusion_weight:.2f})"
                )
                changed = True

        return facts_with_weights, explanations