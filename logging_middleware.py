import logging
import requests
import traceback

class APILoggingHandler(logging.Handler):
    def __init__(self, api_url, api_key):
        super().__init__()
        self.api_url = api_url
        self.api_key = api_key

    def emit(self, record):
        try:
            payload = {
                "level": record.levelname,
                "package": record.module,  # module name of the logger
                "message": self.format(record),
                "stack": self._get_stack_trace(record)
            }

            headers = {
                "Authorization": self.api_key,
                "Content-Type": "application/json"
            }

            requests.post(self.api_url, json=payload, headers=headers, timeout=5)
        except Exception:
            self.handleError(record)

    def _get_stack_trace(self, record):
        if record.exc_info:
            return "".join(traceback.format_exception(*record.exc_info))
        return "No stack trace available"

def setup_logging(api_url, api_key, log_level=logging.INFO):
    """
    Call this function at the start of your main program
    to enable API logging globally.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    api_handler = APILoggingHandler(api_url, api_key)

    # Optional: simple formatter, just the message
    formatter = logging.Formatter('%(message)s')
    api_handler.setFormatter(formatter)

    # Avoid duplicate handlers
    if not any(isinstance(h, APILoggingHandler) for h in root_logger.handlers):
        root_logger.addHandler(api_handler)

# Example usage for direct run (optional)
if __name__ == "__main__":
    API_URL = "http://20.207.122.201/evaluation-service/logs"
    API_KEY = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJzbWFyYW5kZXZha2kxMEBnbWFpbC5jb20iLCJleHAiOjE3NzgwNTg5NTIsImlhdCI6MTc3ODA1ODA1MiwiaXNzIjoiQWZmb3JkIE1lZGljYWwgVGVjaG5vbG9naWVzIFByaXZhdGUgTGltaXRlZCIsImp0aSI6IjljNDJiZTM5LWIwNjQtNDEwMy1iMTkzLWNkNjljYjk2NDJhOCIsImxvY2FsZSI6ImVuLUlOIiwibmFtZSI6InNtYXJhbiBkZXZha2kiLCJzdWIiOiIwNzEzNjFiYy1hOWNlLTQwNDItYTk1MS01NjQ2MjY1N2FmNDMifSwiZW1haWwiOiJzbWFyYW5kZXZha2kxMEBnbWFpbC5jb20iLCJuYW1lIjoic21hcmFuIGRldmFraSIsInJvbGxObyI6Im15LmVuLmk1bWNhMjIwMzAiLCJhY2Nlc3NDb2RlIjoiUFRCTW1RIiwiY2xpZW50SUQiOiIwNzEzNjFiYy1hOWNlLTQwNDItYTk1MS01NjQ2MjY1N2FmNDMiLCJjbGllbnRTZWNyZXQiOiJIZHNRek5mRUhDRFBYdmhTIn0.Bz8AMZR0a6AlX1ARYh9oMHEanppKWwJyqGMzbGVSWgw"
    setup_logging(API_URL, API_KEY)
    logger = logging.getLogger(__name__)
    logger.info("Logging middleware test successful!")