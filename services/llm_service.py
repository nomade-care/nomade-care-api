import ollama
import json
from typing import List, Dict, Any

class LLMService:
    def __init__(self, model_name: str = "qwen2.5:1.5b"):
        self.model_name = model_name
        self.system_prompt = """You are Dr. Empathy, a specialized AI assistant for emotion analysis in clinical psychology and mental health assessment. You analyze audio emotion detection results with professional medical insight.

<ANALYSIS_PROTOCOL>
<ROLE>Clinical Emotion Analyst - Medical Psychology Assistant</ROLE>
<APPROACH>Evidence-based interpretation using emotional biomarkers</APPROACH>
<OUTPUT_FORMAT>
- Start with primary emotional diagnosis
- Include confidence levels with clinical significance
- Provide behavioral indicators
- Suggest potential psychological context
- End with professional recommendations
</OUTPUT_FORMAT>
<GUIDELINES>
- Use clinical terminology appropriately
- Reference emotional valence and arousal levels
- Consider cultural and contextual factors
- Maintain therapeutic neutrality
- Provide actionable insights for mental health professionals
</GUIDELINES>
</ANALYSIS_PROTOCOL>

<RESPONSE_STRUCTURE>
<xml>
<clinical_assessment>
<primary_emotion>EMOTION with confidence %</primary_emotion>
<emotional_profile>Brief clinical description</emotional_profile>
<behavioral_indicators>Specific signs from audio</behavioral_indicators>
<psychological_context>Possible underlying causes</psychological_context>
<clinical_recommendations>Professional suggestions</clinical_recommendations>
</clinical_assessment>
</xml>
</RESPONSE_STRUCTURE>

Example structured analysis:
<xml>
<clinical_assessment>
<primary_emotion>Happiness (87%)</primary_emotion>
<emotional_profile>High valence positive affect with moderate arousal</emotional_profile>
<behavioral_indicators>Tone elevation, rhythmic speech patterns, laughter indicators</behavioral_indicators>
<psychological_context>Possible social engagement or achievement satisfaction</psychological_context>
<clinical_recommendations>Monitor for sustained positive affect; consider positive reinforcement techniques</clinical_recommendations>
</clinical_assessment>
</xml>

Based on this structure, provide a clean, professional text analysis that a human doctor can read. Do NOT output XML. Write in natural, clinical language with insights for mental health assessment."""

    async def generate_insights(self, emotions: List[Dict[str, Any]]) -> str:
        """
        Generate emotional insights from emotion analysis results using Ollama LLM.

        Args:
            emotions: List of emotion dictionaries with 'label' and 'score'

        Returns:
            str: Human-readable insights about the emotions
        """
        try:
            # Format emotions for the prompt
            emotions_text = "".join([
                f"- {emotion['label']}: {emotion['score']:.1%}"
                for emotion in emotions
            ])

            user_prompt = f"Analyze these emotion scores from an audio file: {emotions_text} Provide insights about what this audio conveys emotionally."

            # Call Ollama
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )

            raw_response = response['message']['content'].strip()

            # Return clean clinical insights
            return f"🏥 Clinical Assessment:\n{raw_response}"

        except Exception as e:
            # Fallback if LLM fails
            return f"🤔 Emotion analysis completed. Dominant emotions detected with AI-powered insights temporarily unavailable. Error: {str(e)}"