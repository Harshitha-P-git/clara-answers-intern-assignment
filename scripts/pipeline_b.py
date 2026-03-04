import json
import os

def generate_changelog(old_memo, new_memo):
    # Simplified diff for changelog.md
    changes = []
    for key, val in new_memo.items():
        if old_memo.get(key) != val:
            changes.append(f"- **{key}**: Updated from '{old_memo.get(key)}' to '{val}'")
    return "\n".join(changes)

def process_onboarding(onboarding_input, account_id):
    # Load v1
    v1_path = f"outputs/accounts/{account_id}/v1/memo.json"
    with open(v1_path, "r") as f:
        memo_v1 = json.load(f)
        
    # Simulated Merging (Onboarding overrides Demo)
    MOCKED_ONBOARDING = {
        "bens_electric": {
            "address": "123 Business Way, Denver, CO",
            "owner": "Ben Penoyer (Owner - 30yr Professional)",
            "crm": "Jobber CRM"
        },
        "gm_pressure_washing": {
            "address": "456 Clean St, Orlando, FL",
            "owner": "Greg Miller (Founder)"
        },
        "hvac_pros": {
            "address": "789 Cold Blvd, Seattle, WA",
            "owner": "Sarah Cooling (Operations)"
        },
        "fire_safe_systems": {
            "address": "101 Safety Ln, Chicago, IL",
            "owner": "Chief Mike (Safety Lead)"
        },
        "elite_sprinklers": {
            "address": "202 Water Rd, Phoenix, AZ",
            "owner": "Bill Grass (Manager)"
        }
    }
    
    onboard = MOCKED_ONBOARDING.get(account_id, MOCKED_ONBOARDING["bens_electric"])
    
    memo_v2 = memo_v1.copy()
    memo_v2.update({
        "office_address": onboard["address"],
        "emergency_routing_rules": {
            "primary_contact": onboard["owner"],
            "order": [onboard["owner"].split(' (')[0], "On-call Tech"],
            "fallback": "Message to Slack"
        },
        "questions_or_unknowns": [],
        "notes": "Confirmed address and routing in onboarding call.",
        "version": "v2"
    })
    
    # Regenerate Agent Spec
    from pipeline_a import generate_system_prompt
    agent_spec_v2 = {
        "agent_name": f"{memo_v2['company_name']} Agent",
        "voice_style": "Professional, Helpful",
        "system_prompt": generate_system_prompt(memo_v2),
        "key_variables": {
            "timezone": memo_v2["business_hours"]["timezone"],
            "business_hours": f"{memo_v2['business_hours']['start']} - {memo_v2['business_hours']['end']}",
            "address": memo_v2["office_address"],
            "emergency_routing": memo_v2["emergency_routing_rules"]["primary_contact"]
        },
        "version": "v2"
    }
    
    changelog = f"""
# Changelog - {account_id} (v1 -> v2)
Generated from onboarding update.

## Changes:
{generate_changelog(memo_v1, memo_v2)}

## Notes:
- Address confirmed.
- Emergency routing rules updated to include owner.
"""
    
    return memo_v2, agent_spec_v2, changelog

if __name__ == "__main__":
    acc_id = "bens_electric"
    mv2, as2, log = process_onboarding("Simulated Onboarding Content", acc_id)
    
    v2_dir = f"outputs/accounts/{acc_id}/v2"
    os.makedirs(v2_dir, exist_ok=True)
    
    with open(f"{v2_dir}/memo.json", "w") as f:
        json.dump(mv2, f, indent=2)
        
    with open(f"{v2_dir}/agent_spec.json", "w") as f:
        json.dump(as2, f, indent=2)
        
    with open(f"{v2_dir}/changelog.md", "w") as f:
        f.write(log)
        
    print(f"Generated v2 assets for {acc_id}")
