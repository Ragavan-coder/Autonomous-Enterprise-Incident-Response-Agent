import sys
import time
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app.agents.incident_manager import trigger_investigation

def print_step(step, delay=1.0):
    print(f"\n[ {time.strftime('%H:%M:%S')} ] {step}")
    time.sleep(delay)

def run_demo():
    print("==================================================")
    print("AUTONOMOUS ENTERPRISE INCIDENT RESPONSE AGENT DEMO")
    print("==================================================")
    
    incident = {
        "title": "Checkout error rate increased to 18%",
        "description": "Checkout error rate increased from 1.2% to 18%",
        "service": "checkout-service",
        "severity": "SEV1"
    }
    
    print_step(f"INCIDENT CREATED: {incident['title']}")
    print_step(f"AI Triage - Classifying as SEV1, Affected service: {incident['service']}")
    print_step("Investigation Agent starting...")
    
    trace = trigger_investigation(incident)
    
    for t in trace:
        agent = t.get('agent')
        if agent == 'tool_execution':
            print_step(f"Investigation Agent called {t.get('tool')} with args: {t.get('args')}", 0.5)
        elif agent == 'tool_result':
            # truncate result
            res = t.get('result', '')
            if len(res) > 80:
                res = res[:77] + "..."
            print_step(f"Tool {t.get('tool')} returned: {res}", 0.5)
        elif agent == 'root_cause_analyzer':
            print_step("Root Cause Agent forming hypothesis based on evidence...")
            print_step(f"Root Cause Analysis Output:\n{t.get('content')}")
            
    print_step("Remediation Agent proposed rollback of payment-service v4.8.2. Risk: HIGH.")
    print_step("WAITING FOR HUMAN APPROVAL...")
    time.sleep(1)
    
    print_step("HUMAN APPROVED action.")
    print_step("SIMULATED ROLLBACK STARTED for payment-service.")
    time.sleep(1)
    
    print_step("ROLLBACK COMPLETED.")
    print_step("Verification: Error rate is now 1.4%. PASSED.")
    print_step("Postmortem Agent generating incident summary...")
    print_step("DEMO COMPLETED.")

if __name__ == "__main__":
    run_demo()
