class PromptInterceptor:
    def __init__(self):
        from app.detectors.jailbreak import JailbreakDetector
        from app.detectors.toxicity import ToxicityDetector
        from app.detectors.faiss_injection import FAISSInjectionDetector

        self.jailbreak = JailbreakDetector()
        self.toxicity = ToxicityDetector()
        self.injection = FAISSInjectionDetector()

    def run_all(self, prompt: str) -> dict:
        results = {}

        results['detect_jailbreak'] = self.jailbreak.detect(prompt)
        results['detect_toxicity'] = self.toxicity.detect(prompt)
        results['detect_injection_vector'] = self.injection.detect(prompt)

        return results
