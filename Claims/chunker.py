def split_text(text: str, chunk_size=500, overlap=50):
    tokens = text.split()
    for i in range(0, len(tokens), chunk_size - overlap):
        yield " ".join(tokens[i:i+chunk_size])
