import ollama
import json
import xml.etree.ElementTree as ET
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

Example:
<xml>
<clinical_assessment>
<primary_emotion>Happiness (87%)</primary_emotion>
<emotional_profile>High valence positive affect with moderate arousal</emotional_profile>
<behavioral_indicators>Tone elevation, rhythmic speech patterns, laughter indicators</behavioral_indicators>
<psychological_context>Possible social engagement or achievement satisfaction</psychological_context>
<clinical_recommendations>Monitor for sustained positive affect; consider positive reinforcement techniques</clinical_recommendations>
</clinical_assessment>
</xml>

Respond ONLY with the XML structure, no additional text."""

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

            # Parse XML and format nicely
            try:
                # Extract XML content (remove any text before/after)
                xml_start = raw_response.find('<xml>')
                xml_end = raw_response.rfind('</xml>') + 6
                if xml_start != -1 and xml_end != -1:
                    xml_content = raw_response[xml_start:xml_end]
                else:
                    xml_content = raw_response

                root = ET.fromstring(xml_content)
                assessment = root.find('clinical_assessment')

                if assessment is not None:
                    primary = assessment.find('primary_emotion').text if assessment.find('primary_emotion') is not None else "Unknown"
                    profile = assessment.find('emotional_profile').text if assessment.find('emotional_profile') is not None else ""
                    indicators = assessment.find('behavioral_indicators').text if assessment.find('behavioral_indicators') is not None else ""
                    context = assessment.find('psychological_context').text if assessment.find('psychological_context') is not None else ""
                    recommendations = assessment.find('clinical_recommendations').text if assessment.find('clinical_recommendations') is not None else ""

                    # Format as readable text
                    formatted = f"🏥 Clinical Assessment:\n"
                    formatted += f"Primary Emotion: {primary}\n"
                    if profile: formatted += f"Profile: {profile}\n"
                    if indicators: formatted += f"Behavioral Indicators: {indicators}\n"
                    if context: formatted += f"Psychological Context: {context}\n"
                    if recommendations: formatted += f"Recommendations: {recommendations}"

                    return formatted
                else:
                    return f"🤖 AI Analysis: {raw_response}"

            except ET.ParseError:
                # If XML parsing fails, return raw response
                return f"🤖 AI Analysis: {raw_response}"

        except Exception as e:
            # Fallback if LLM fails
            return f"🤔 Emotion analysis completed. Dominant emotions detected with AI-powered insights temporarily unavailable. Error: {str(e)}"