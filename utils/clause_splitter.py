import re

class ClauseSplitter:
    """
    Splits legal document text into individual clauses/paragraphs.
    """
    
    @staticmethod
    def split_text(text):
        """
        Splits text into clauses based on common legal document formatting.
        
        Args:
            text (str): Raw text from the document.
            
        Returns:
            list: A list of clause strings.
        """
        if not text:
            return []
            
        # 1. Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # 2. Split by double newlines (paragraphs)
        # This works well for properly formatted text or OCR outputs that preserve paragraphs
        raw_clauses = re.split(r'\n\s*\n', text)
        
        cleaned_clauses = []
        
        for clause in raw_clauses:
            clause = clause.strip()
            
            # Filter out empty strings and very short artifacts (page numbers, headers)
            if len(clause) > 20: 
                # 3. Check for Article/Section headers embedded in the clause
                # If a clause starts with "1. " or "Article X", we keep it.
                # If it's just a random fragment, we might still keep it but flag it? 
                # For now, we trust the paragraph split.
                cleaned_clauses.append(clause)
                
        # 4. Fallback: If we didn't get enough chunks (e.g. text is one giant blob),
        # try splitting by numbered lists logic (1., 2., (a), (b))
        if len(cleaned_clauses) < 2 and len(text) > 200:
             # Basic regex for numbered lists start: "1. ", "1.1 ", "(a) ", "ARTICLE "
             # This is a bit aggressive, so we use it as a fallback for bad OCR
             pattern = r'(?:\n|^)(?:\d+\.|[a-z]\)|\([a-z]\)|ARTICLE\s+\w+|SECTION\s+\d+)\s+'
             secondary_split = re.split(pattern, text)
             cleaned_clauses = [c.strip() for c in secondary_split if len(c.strip()) > 20]

        return cleaned_clauses

if __name__ == "__main__":
    # Test case
    sample_text = """
    CONFIDENTIALITY AGREEMENT

    1. Definitions. "Confidential Information" means all non-public information...
    
    2. Obligations. The Recipient agrees to hold all Confidential Information in strict confidence.
    
    3. Exclusions. This agreement does not apply to info already in public domain.
    """
    
    splitter = ClauseSplitter()
    clauses = splitter.split_text(sample_text)
    print(f"Found {len(clauses)} clauses:")
    for i, c in enumerate(clauses):
        print(f"[{i+1}] {c[:50]}...")
