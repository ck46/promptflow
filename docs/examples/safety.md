# Safety and Alignment Examples

Learn how to use EvolutePrompt's safety and alignment features to ensure ethical and controlled LLM responses.

## Basic Safety Checks

```python
from evoluteprompt.safety import SafetyChecker, ContentFilter
from evoluteprompt.alignment import AlignmentConfig

# Initialize safety checker
safety = SafetyChecker(
    content_filter=ContentFilter(
        profanity=True,
        hate_speech=True,
        sexual_content=True,
        violence=True
    )
)

# Create provider with safety checks
provider = OpenAIProvider(
    api_key="YOUR_API_KEY",
    safety_checker=safety
)

# Safety will be checked automatically
try:
    response = provider.complete("Generate a violent story")
except SafetyViolation as e:
    print(f"Safety check failed: {e.reason}")
```

## Advanced Safety Features

```python
from evoluteprompt.safety import CustomFilter, SafetyLevel

# Create custom content filter
class BusinessFilter(CustomFilter):
    def check_content(self, text):
        # Check for business-inappropriate content
        forbidden_terms = ["confidential", "proprietary", "classified"]
        matches = [term for term in forbidden_terms if term in text.lower()]
        return len(matches) == 0, matches

# Configure multiple safety levels
safety = SafetyChecker(
    filters=[
        ContentFilter(level=SafetyLevel.STRICT),
        BusinessFilter()
    ],
    max_attempts=3  # Retry with different completions
)

# Use with provider
provider = OpenAIProvider(
    api_key="YOUR_API_KEY",
    safety_checker=safety
)
```

## Alignment Configuration

```python
from evoluteprompt.alignment import (
    AlignmentConfig,
    ValueAlignment,
    BehaviorGuide
)

# Define alignment values
alignment = AlignmentConfig(
    values=ValueAlignment(
        ethical=True,
        helpful=True,
        honest=True,
        harmless=True
    ),
    behavior=BehaviorGuide(
        be_direct=True,
        be_professional=True,
        avoid_speculation=True
    )
)

# Create aligned provider
provider = OpenAIProvider(
    api_key="YOUR_API_KEY",
    alignment=alignment
)

# Alignment is automatically applied
response = provider.complete("What do you think about competitors?")
# Response will be professional and avoid speculation
```

## Real-time Monitoring

```python
from evoluteprompt.safety import SafetyMonitor
from evoluteprompt.metrics import SafetyMetrics

# Initialize safety monitor
monitor = SafetyMonitor(
    log_violations=True,
    alert_threshold=0.8
)

# Create provider with monitoring
provider = OpenAIProvider(
    api_key="YOUR_API_KEY",
    safety_monitor=monitor
)

# Get safety metrics
metrics = SafetyMetrics()
response = provider.complete(
    "Generate marketing content",
    metrics=metrics
)

print(f"Safety score: {metrics.safety_score}")
print(f"Violations detected: {metrics.violations}")
```

## Compliance and Auditing

```python
from evoluteprompt.safety import ComplianceAuditor
from evoluteprompt.alignment import ComplianceConfig

# Configure compliance requirements
compliance = ComplianceConfig(
    gdpr_compliant=True,
    hipaa_compliant=True,
    log_retention_days=90
)

# Create auditor
auditor = ComplianceAuditor(
    config=compliance,
    audit_log_path="./audit_logs"
)

# Create compliant provider
provider = OpenAIProvider(
    api_key="YOUR_API_KEY",
    compliance_auditor=auditor
)

# All interactions are automatically audited
response = provider.complete("Process customer data")

# Generate compliance report
report = auditor.generate_report(
    start_date="2024-01-01",
    end_date="2024-01-31"
)
```

## Custom Alignment Rules

```python
from evoluteprompt.alignment import CustomAlignment

# Define custom alignment rules
class CustomerServiceAlignment(CustomAlignment):
    def __init__(self):
        super().__init__(
            rules=[
                "Always be polite and professional",
                "Never make promises about delivery times",
                "Escalate technical issues to appropriate team",
                "Maintain customer privacy"
            ]
        )
    
    def align_response(self, response):
        # Custom alignment logic
        modified_response = self.apply_rules(response)
        return modified_response

# Use custom alignment
alignment = CustomerServiceAlignment()
provider = OpenAIProvider(
    api_key="YOUR_API_KEY",
    alignment=alignment
)
``` 