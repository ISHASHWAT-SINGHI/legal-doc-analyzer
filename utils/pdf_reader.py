import PyPDF2
import os

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not a valid PDF or encrypted.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    text = []
    
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            
            # Check if encrypted - simplified check
            if reader.is_encrypted:
                try:
                    reader.decrypt("")
                except:
                     # If generic decryption fails, warn user (in a real app, we'd handle passwords)
                    print(f"Warning: {file_path} is encrypted. Attempting to read anyway.")

            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
                else:
                    print(f"Warning: No text found on page {page_num + 1}")

    except Exception as e:
        raise ValueError(f"Error reading PDF: {str(e)}")

    full_text = "\n".join(text)
    
    if not full_text.strip():
         raise ValueError("PDF contains no extractable text. It might be scanned/image-based.")

    return full_text

if __name__ == "__main__":
    # Simple test execution
    import sys
    if len(sys.argv) > 1:
        print(extract_text_from_pdf(sys.argv[1])[:500] + "...")
    else:
        print("Usage: python pdf_reader.py <path_to_pdf>")
