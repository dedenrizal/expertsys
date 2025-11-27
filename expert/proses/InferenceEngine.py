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
            print(avg_weight)
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
    
    def evaluate_condition_backward(self, condition, fact_with_weight):
        cond_type = condition.get("type", "and")
        items = condition["items"]

        if cond_type == 'AND':
            total_weight = 0
            count = 0
            for item in items:
                fact = item["fact"]
                required_weight = item.get("weight", 1.0)
                
                is_true, weight = self.backward_chain(fact, fact_with_weight)
                if is_true and weight < required_weight:
                    return False, 0
                total_weight += weight
                count += 1
            avg_weight = total_weight / count if count > 0 else 0
            print(avg_weight)
            return True, avg_weight
        
        elif cond_type == "OR":
            for item in items:
                fact = item["fact"]
                required_weight = item.get("weight", 1.0)
                print(required_weight)

                is_true, weight = self.backward_chain(fact, fact_with_weight)
                if is_true and weight >=required_weight:
                    return True, weight
            return False,0
        
        elif cond_type == "NOT":
            for item in items:
                fact = item["fact"]
                print(fact)
                is_true, _ = self.backward_chain(fact, fact_with_weight)
                if is_true: 
                    return False,0
            return True, 1.0
        return False, 0


    def forward_chain(self, initial_facts_with_weights):
        facts_with_weights = initial_facts_with_weights.copy()
        explanations = []
        changed = True

        while changed:
            changed = False
            applicable_rules = []
            print(applicable_rules)

            for rule in self.kb.get_all_rules():
                is_satisfied, condition_weight = self.evaluate_condition(rule.conditions, facts_with_weights)
                conclusion_fact = rule.conclusion["fact"]
                conclusion_weight = rule.conclusion["weight"]
                priority = rule.priority

                if is_satisfied and conclusion_fact not in facts_with_weights:
                    applicable_rules.append((priority, condition_weight, rule))
                    

            if applicable_rules:
                applicable_rules.sort(key=lambda x: x[0], reverse=True)
                _, _, selected_rule = applicable_rules[0]

                conclusion_fact = selected_rule.conclusion["fact"]
                conclusion_weight = selected_rule.conclusion["weight"]
                facts_with_weights[conclusion_fact] = conclusion_weight

                conclusion_obj = self.kb.get_conclusion_by_code(conclusion_fact)
                name = conclusion_obj.name if conclusion_obj else conclusion_fact

                changed = True

        return facts_with_weights, explanations
    
    def backward_chain(self, goal, fact_with_weight):
        if goal in fact_with_weight:
            return True, fact_with_weight[goal]
        
        rules = self.kb.get_all_rules()
        relevant_rules = [rule for rule in rules if rules.conclusion['fact'] == goal]
        relevant_rules.sort(key=lambda r : r.priority, reverse=True)

        for rule in relevant_rules:
            condition = rule.conditions
            conclusion_weight = rule.conclusion["weight"]
            is_satisfied, condition_weight = self.evaluate_condition_bacward(condition, fact_with_weight)

            if is_satisfied:
                return True, min(conclusion_weight, condition_weight)
            
        return False, 0
    