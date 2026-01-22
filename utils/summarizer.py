import re

class Summarizer:
    """
    Generates simplified summaries of legal clauses using 
    heuristic-based rewriting (Rule-based NLP).
    """

    # Dictionary of legalese to plain English
    SIMPLIFICATIONS = {
        r"shall be deemed to be": "will be considered",
        r"shall have the right to": "can",
        r"in the event that": "if",
        r"notwithstanding anything to the contrary": "even if said otherwise",
        r"herein": "in this document",
        r"hereto": "to this agreement",
        r"obligations": "duties",
        r"indemnify": "protect against legal liability",
        r"liable": "responsible",
        r"termination": "cancellation",
        r"pursuant to": "according to",
        r"under no circumstances": "never",
        r"at its sole discretion": "whenever it wants",
        r"null and void": "invalid"
    }

    def summarize(self, text):
        """
        Simplifies legal text by replacing common jargon with plain English.
        
        Args:
            text (str): The original legal text.
            
        Returns:
            str: The simplified text.
        """
        simplified_text = text
        
        # 1. Apply simple replacements
        for pattern, replacement in self.SIMPLIFICATIONS.items():
            # Case insensitive regex replacement
            simplified_text = re.sub(pattern, replacement, simplified_text, flags=re.IGNORECASE)
            
        # 2. Shorten sentence structure (very basic)
        # e.g., "The Provider shall be responsible..." -> "The Provider will be responsible..."
        simplified_text = simplified_text.replace("shall", "will")
        
        # 3. Truncate if too long (for UI purposes)
        if len(simplified_text) > 300:
             simplified_text = simplified_text[:297] + "..."

        return simplified_text.strip()

if __name__ == "__main__":
    # Test
    s = Summarizer()
    print(s.summarize("In the event that the Party is found liable, it shall indemnify the other Party."))
    # Output should be something like: "if the Party is found responsible, it protects against legal liability the other Party."
