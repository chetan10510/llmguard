from app.interceptor import PromptInterceptor
from app.utils.logger import log_prompt_result

prompt = input("Enter your prompt:\n")

interceptor = PromptInterceptor()
results = interceptor.run_all(prompt)
log_prompt_result(prompt, results)

print("\nModeration Result:\n", results)



