from .Logger import setup_logger

file_processor = setup_logger("file_processor")
chain = setup_logger("chain")
pdf_extractor = setup_logger("pdf_extractor")
llm_log = setup_logger("LLM")
llm_tools = setup_logger("LLMTools")
