import re

class RiskAnalyzer:
    """
    Analyzes legal text for potential risks using keyword matching
    and heuristic rules.
    """

    # Define risk keywords/patterns
    HIGH_RISK_KEYWORDS = [
        r"unlimited liability",
        r"indemnify",
        r"indemnification",
        r"waive.*rights",
        r"unilateral.*termination",
        r"dispute.*arbitration",
        r"liquidated damages",
        r"class action waiver"
    ]

    MEDIUM_RISK_KEYWORDS = [
        r"penalty",
        r"automatic renewal",
        r"exclusivity",
        r"non-compete",
        r"jurisdiction.*foreign",
        r"change of control",
        r"termination for convenience"
    ]

    def analyze_risk(self, text):
        """
        Determines the risk level of a given clause text.

        Args:
            text (str): The clause text to analyze.

        Returns:
            dict: {
                "level": "HIGH", "MEDIUM", or "LOW",
                "score": int (0-100),
                "reasons": list of strings (matched patterns)
            }
        """
        text_lower = text.lower()
        score = 0
        reasons = []
        level = "LOW"

        # Check High Risk
        for pattern in self.HIGH_RISK_KEYWORDS:
            if re.search(pattern, text_lower):
                score += 50
                reasons.append(f"High risk term found: '{pattern.replace('.*', ' ')}'")
        
        # Check Medium Risk
        for pattern in self.MEDIUM_RISK_KEYWORDS:
            if re.search(pattern, text_lower):
                score += 20
                reasons.append(f"Medium risk term found: '{pattern.replace('.*', ' ')}'")

        # Heuristic: Length check (Ambiguity check)
        # Extremely long clauses (e.g. > 500 words) might be hiding details
        if len(text.split()) > 400:
             score += 10
             reasons.append("Clause is unusually long (potential ambiguity).")

        # Determine Final Level
        if score >= 50:
            level = "HIGH"
        elif score >= 20:
            level = "MEDIUM"
        
        # Cap score
        score = min(score, 100)

        return {
            "level": level,
            "score": score,
            "reasons": reasons
        }

if __name__ == "__main__":
    # Test cases
    analyzer = RiskAnalyzer()
    
    test_clauses = [
        "The Service Provider shall have unlimited liability for all damages...",
        "This contract shall automatically renew for successive 1-year terms.",
        "The confidentiality obligations shall survive termination.",
        "Simple payment clause with no hidden terms."
    ]

    for c in test_clauses:
        result = analyzer.analyze_risk(c)
        print(f"Clause: {c[:40]}...")
        print(f"Risk: {result['level']} (Score: {result['score']})")
        print(f"Reasons: {result['reasons']}\n")
