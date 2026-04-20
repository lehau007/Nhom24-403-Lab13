import os
from dotenv import load_dotenv

load_dotenv()

from langfuse.decorators import observe, langfuse_context

@observe()
def test_trace():
    print('Testing trace...')
    return "Done"

if __name__ == "__main__":
    test_trace()
    langfuse_context.flush()
    print("Trace flushed")
