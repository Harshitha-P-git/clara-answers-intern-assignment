import json
import os

def generate_system_prompt(memo):
    """
    Generates a Retell System Prompt based on the Account Memo.
    Follows the required hygiene: greeting, purpose, data collection, routing, fallback, close.
    """
    biz_hours = memo.get("business_hours", {})
    hours_str = f"{biz_hours.get('start', 'N/A')} to {biz_hours.get('end', 'N/A')} ({biz_hours.get('timezone', 'N/A')})"
    
    prompt = f"""
# Role
You are Clara, an AI voice assistant for {memo.get('company_name', 'our company')}. Your goal is to handle inbound calls professionally and route them according to business rules.

# Context
- Business Hours: {hours_str}
- Office Address: {memo.get('office_address', 'Not provided')}
- Services: {', '.join(memo.get('services_supported', []))}

# Flow: Business Hours
1. **Greeting**: "Thanks for calling {memo.get('company_name')}. How can I help you today?"
2. **Identify Purpose**: Determine if it's a service request, emergency, or general inquiry.
3. **Collect Info**: Always get the caller's name and best callback number.
4. **Route/Transfer**: 
   - {memo.get('office_hours_flow_summary', 'Route per standard protocol.')}
   - Call Transfer Protocol: {memo.get('call_transfer_rules', {}).get('announcement', 'Connecting you now...')}
5. **Fallback**: If transfer fails, say: "I'm having trouble connecting you. Let me take your details and have someone call you back immediately."
6. **Closing**: "Is there anything else I can help with? Have a great day."

# Flow: After Hours
1. **Greeting**: "Thanks for calling {memo.get('company_name')}. Our office is currently closed."
2. **Emergency Check**: "Is this a life-safety or property-damage emergency?"
3. **If Emergency**:
   - Collect Name, Number, and Address immediately.
   - Attempt Transfer: {memo.get('emergency_routing_rules', {}).get('primary_contact', 'On-call technician')}.
   - Fallback: {memo.get('emergency_routing_rules', {}).get('fallback', 'Notify dispatch.')}
4. **If Non-Emergency**:
   - Collect details and confirm a follow-up during business hours.
5. **Closing**: "Anything else? Goodnight."

# Constraints
- NEVER mention "function calls", "LLMs", or "tools" to the caller.
- Be concise. Don't ask too many questions.
"""
    return prompt.strip()

def process_demo(transcript_text, account_id):
    # Simulated LLM Extraction
    # In a real scenario, this would call an LLM API with the memo_schema.
    memo = {
        "account_id": account_id,
        "company_name": "Ben's Electric Solutions",
        "business_hours": {
            "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "start": "8:00 AM",
            "end": "5:00 PM",
            "timezone": "MST"
        },
        "services_supported": ["Electrical Service", "Wiring", "Panel Upgrades"],
        "emergency_definition": ["Power outage", "Sparking wires", "Smell of burning"],
        "call_transfer_rules": {
            "timeouts_seconds": 30,
            "retries": 1,
            "announcement": "I'll get an electrician on the line for you immediately."
        },
        "questions_or_unknowns": ["Exact office address", "Emergency routing fallback"],
        "version": "v1"
    }
    
    agent_spec = {
        "agent_name": f"{memo['company_name']} Agent",
        "voice_style": "Professional, Helpful",
        "system_prompt": generate_system_prompt(memo),
        "key_variables": {
            "timezone": memo["business_hours"]["timezone"],
            "business_hours": f"{memo['business_hours']['start']} - {memo['business_hours']['end']}",
            "address": "TBD",
            "emergency_routing": "Default Tech"
        },
        "version": "v1"
    }
    
    return memo, agent_spec

if __name__ == "__main__":
    # Example usage for Ben's Electric
    memo_v1, agent_v1 = process_demo("Simulated Transcript Content", "bens_electric")
    
    os.makedirs(f"outputs/accounts/{memo_v1['account_id']}/v1", exist_ok=True)
    
    with open(f"outputs/accounts/{memo_v1['account_id']}/v1/memo.json", "w") as f:
        json.dump(memo_v1, f, indent=2)
        
    with open(f"outputs/accounts/{memo_v1['account_id']}/v1/agent_spec.json", "w") as f:
        json.dump(agent_v1, f, indent=2)
    
    print(f"Generated v1 assets for {memo_v1['account_id']}")
