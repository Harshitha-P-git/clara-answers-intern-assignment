import json
import os
from pipeline_a import process_demo
from pipeline_b import process_onboarding

def run_batch():
    # Simulated dataset of 5 accounts (Demo + Onboarding each)
    accounts = [
        "bens_electric",
        "gm_pressure_washing",
        "hvac_pros",
        "fire_safe_systems",
        "elite_sprinklers"
    ]
    
    tasks = []
    
    for acc in accounts:
        print(f"Processing Account: {acc}...")
        
        # Pipeline A: Demo -> v1
        memo_v1, agent_v1 = process_demo(f"Transcript for {acc} demo", acc)
        v1_dir = f"outputs/accounts/{acc}/v1"
        os.makedirs(v1_dir, exist_ok=True)
        with open(f"{v1_dir}/memo.json", "w") as f: json.dump(memo_v1, f, indent=2)
        with open(f"{v1_dir}/agent_spec.json", "w") as f: json.dump(agent_v1, f, indent=2)
        
        # Add to task tracker
        tasks.append({"account_id": acc, "stage": "v1_complete", "status": "Success"})
        
        # Pipeline B: Onboarding -> v2
        memo_v2, agent_v2, log = process_onboarding(f"Onboarding data for {acc}", acc)
        v2_dir = f"outputs/accounts/{acc}/v2"
        os.makedirs(v2_dir, exist_ok=True)
        with open(f"{v2_dir}/memo.json", "w") as f: json.dump(memo_v2, f, indent=2)
        with open(f"{v2_dir}/agent_spec.json", "w") as f: json.dump(agent_v2, f, indent=2)
        with open(f"{v2_dir}/changelog.md", "w") as f: f.write(log)
        
        tasks.append({"account_id": acc, "stage": "v2_complete", "status": "Success"})
        
    # Calculate Summary Metrics
    metrics = {
        "total_accounts": len(accounts),
        "total_files_processed": len(accounts) * 2,
        "success_rate": "100%",
        "stages": {
            "v1_demo": len([t for t in tasks if t['stage'] == 'v1_complete']),
            "v2_onboarding": len([t for t in tasks if t['stage'] == 'v2_complete'])
        }
    }
    
    # Save metrics and task tracker
    with open("outputs/tasks.json", "w") as f:
        json.dump({"metrics": metrics, "tasks": tasks}, f, indent=2)
    
    print(f"\nBatch processing complete for all {metrics['total_files_processed']} files.")
    print("Summary Metrics & Task tracker updated: outputs/tasks.json")

if __name__ == "__main__":
    run_batch()
