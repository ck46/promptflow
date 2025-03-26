# Experimentation & Analytics Examples

Learn how to use EvolutePrompt's experimentation and analytics features to optimize your prompts.

## Running Experiments

```python
from evoluteprompt import Experiment, MetricsCollector
from evoluteprompt.metrics import ResponseQuality, Latency, TokenUsage

# Create an experiment
experiment = Experiment(
    name="customer_service_optimization",
    description="Testing different prompt variations for customer service"
)

# Define prompt variations
variations = [
    PromptBuilder()\
        .add_system("You are a friendly customer service agent.")\
        .add_user("How can I reset my password?")\
        .build(),
    PromptBuilder()\
        .add_system("You are a technical support specialist.")\
        .add_user("How can I reset my password?")\
        .build()
]

# Set up metrics collection
metrics = MetricsCollector([
    ResponseQuality(),
    Latency(),
    TokenUsage()
])

# Run the experiment
results = experiment.run_variations(
    variations=variations,
    provider=llm_provider,
    metrics=metrics,
    sample_size=100
)
```

## Analyzing Results

```python
# Get experiment results
summary = results.get_summary()
print(f"Best performing variation: {summary.best_variation}")
print(f"Performance improvement: {summary.improvement_percentage}%")

# Detailed metrics analysis
metrics_breakdown = results.get_metrics_breakdown()
for metric in metrics_breakdown:
    print(f"{metric.name}: {metric.value}")

# Visualize results
results.plot_metrics()
results.plot_comparison()

# Export results
results.export_to_csv("experiment_results.csv")
```

## A/B Testing

```python
from evoluteprompt.testing import ABTest

# Set up A/B test
ab_test = ABTest(
    control_prompt=original_prompt,
    test_prompt=new_prompt,
    success_metric="response_quality",
    sample_size=1000
)

# Run the test
test_results = ab_test.run()

# Statistical analysis
significance = test_results.get_statistical_significance()
print(f"P-value: {significance.p_value}")
print(f"Confidence interval: {significance.confidence_interval}")
```

## Custom Metrics

```python
from evoluteprompt.metrics import CustomMetric

class SentimentScore(CustomMetric):
    def calculate(self, response):
        # Custom logic to calculate sentiment
        sentiment_score = analyze_sentiment(response.text)
        return sentiment_score

# Add custom metric to experiment
custom_metrics = MetricsCollector([
    SentimentScore(),
    ResponseQuality()
])

# Run experiment with custom metrics
results = experiment.run_variations(
    variations=variations,
    metrics=custom_metrics
)
``` 