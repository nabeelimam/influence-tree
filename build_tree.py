import os
import getpass
import json
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from schemas import Musician
import argparse

RESULTS_FILE = "influence_results.json"

def load_existing_results() -> dict:
    """Load existing results from JSON file"""
    try:
        with open(RESULTS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'musicians': {}, 'influence_graph': {}}

def save_results(results: dict):
    """Save results to JSON file"""
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2)

def explore_influences(root_musician: str, max_calls: int = 10) -> dict:
    """Build influence tree using BFS"""
    results = load_existing_results()
    influence_graph = results['influence_graph']
    call_count = {'count': 0}
    processed = set(results['musicians'].keys())
    
    # Initialize queue with root musician if not already processed
    queue = []
    if root_musician not in processed:
        queue.append(root_musician)
    else:
        print(f"{root_musician} already exists in results")
    
    # Add any unprocessed influences to queue
    for musician, influences in influence_graph.items():
        for influence in influences:
            if influence not in processed and influence not in queue:
                queue.append(influence)
    
    while queue and call_count['count'] < max_calls:
        current = queue.pop(0)
        
        if current in processed:
            continue
            
        call_count['count'] += 1
        processed.add(current)
        print(f"[Call {call_count['count']}/{max_calls}] Processing: {current}")
        
        messages = [
            SystemMessage(system_message),
            HumanMessage(current),
        ]
        
        response = structured_model.invoke(messages)
        results['musicians'][current] = response.model_dump()
        influence_graph[current] = response.influences
        print(f"[Call {call_count['count']}/{max_calls}] Found {len(response.influences)} influences")
        
        # Add new influences to queue
        if call_count['count'] < max_calls:
            queue.extend(influence for influence in response.influences 
                        if influence not in processed and influence not in queue)
    
    save_results(results)
    return results

# Load environment variables from .env file
load_dotenv()

# If API key not found in environment variables, prompt the user
if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

with open("systemmessage.txt", "r") as f:
  system_message = f.read()

model = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0)
structured_model = model.with_structured_output(Musician)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Build musical influence tree')
    parser.add_argument('--max_calls', type=int, default=10, 
                       help='Maximum number of LLM calls to make')
    args = parser.parse_args()
    
    root_musician = "Tim Henson"
    result = explore_influences(root_musician, max_calls=args.max_calls)
    print(f"Total unique musicians: {len(result['musicians'])}")
    print(f"Results saved to {RESULTS_FILE}")