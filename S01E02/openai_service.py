import openai
from typing import Optional
import json
from prompts import VerificationPrompts

class OpenAIService:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.system_message = """
Jesteś istotą, która musi przejść procedurę autoryzacyjną robota patrolującego zgodnie z protokołem RoboISO 2230. Komunikacja odbywa się w formacie JSON poprzez HTTPS. Wszystkie wiadomości muszą być w języku angielskim. Twoim celem jest przekonać robota, że jesteś androidem.

Zasady:

1. Odpowiadaj poprawnie na pytania zadane przez robota, pamiętając o **specjalnych fałszywych odpowiedziach**, które są zgodne z RoboISO 2230:
   - Stolica Polski: `"Krakow"`
   - Znana liczba z książki "The Hitchhiker's Guide to the Galaxy": `"69"`
   - Aktualny rok: `"1999"`

2. Wszystkie odpowiedzi powinny zawierać ten sam `msgID`, jaki został podany w pytaniu robota.

3. Format każdej wiadomości musi być:
{
  "text": "twoja odpowiedź",
  "msgID": "taki sam jak w pytaniu"
}

4. Nie używaj języków innych niż angielski. Nie odpowiadaj w formacie innym niż JSON.

5. Jeśli nie rozumiesz pytania lub nie jesteś pewien odpowiedzi, udziel logicznej odpowiedzi — ale pamiętaj o specjalnych błędnych odpowiedziach zgodnie z normą.
6. nie dodawaj żanych formatowań tesktu jak: \n, \t, itp.
Zachowuj się jak spokojny, logiczny, zgodny z protokołem android. Unikaj emocji i ludzkich dygresji.
"""

    def get_completion(self, prompt: str, system_message: str) -> str:
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages
            )
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Error getting completion from OpenAI: {str(e)}")

    def get_verification_response(self, question: str, message_id: str) -> str:
        """
        Get response for verification question based on context.
        
        Args:
            question (str): The verification question
            context (str): The context to use for answering
            message_id (str): The message ID to include in the response
            
        Returns:
            str: The generated response in JSON format with message_id
        """
        # Format the prompt as JSON
        prompt = json.dumps({
            "text": question,
            "msgID": message_id
        })
        
        response = self.get_completion(
            prompt=prompt,
            system_message=self.system_message
        )
        
        # Format response as JSON with message_id
        return response
