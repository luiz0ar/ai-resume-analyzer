import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "ai_resume_analyzer",
    level: str = "INFO",
    log_format: Optional[str] = None,
) -> logging.Logger:
   
    if log_format is None:
        log_format = (
            "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
        )
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    if logger.handlers:
        return logger
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    logger.propagate = False
    
    return logger


def read_prompt_file(file_path: Path) -> str:

    logger = logging.getLogger(__name__)
    
    if not file_path.exists():
        logger.error("Prompt file not found: %s", file_path)
        raise FileNotFoundError(f"Prompt file not found: {file_path}")
    
    try:
        content = file_path.read_text(encoding="utf-8")
        logger.debug("Successfully loaded prompt file: %s", file_path)
        return content.strip()
    except IOError as e:
        logger.error("Failed to read prompt file %s: %s", file_path, str(e))
        raise


def read_file_content(file_path: Path) -> str:

    logger = logging.getLogger(__name__)
    
    if not file_path.exists():
        logger.error("File not found: %s", file_path)
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        content = file_path.read_text(encoding="utf-8")
        logger.debug("Successfully read file: %s (%d chars)", file_path, len(content))
        return content
    except IOError as e:
        logger.error("Failed to read file %s: %s", file_path, str(e))
        raise


def save_json_result(file_path: Path, content: str) -> None:

    logger = logging.getLogger(__name__)
    
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_path.write_text(content, encoding="utf-8")
        logger.info("Successfully saved result to: %s", file_path)
    except IOError as e:
        logger.error("Failed to save file %s: %s", file_path, str(e))
        raise


def validate_api_key(api_key: str) -> bool:

    if not api_key:
        return False
    
    return api_key.startswith("sk-") and len(api_key) > 20
