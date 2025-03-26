# Prompt Testing Examples

Learn how to use EvolutePrompt's testing framework to ensure prompt quality and reliability.

## Basic Testing

```python
from evoluteprompt.testing import PromptTest, TestCase, assert_response

class CustomerServiceTest(PromptTest):
    def test_greeting(self):
        prompt = PromptBuilder()\
            .add_system("You are a customer service agent.")\
            .add_user("Hello, I need help.")\
            .build()
        
        response = self.provider.complete(prompt)
        
        # Assert response contains greeting
        assert_response(response).contains(
            ["hello", "hi", "greetings"],
            case_insensitive=True
        )
    
    def test_problem_solving(self):
        prompt = PromptBuilder()\
            .add_system("You are a technical support agent.")\
            .add_user("My internet is not working.")\
            .build()
        
        response = self.provider.complete(prompt)
        
        # Assert response structure
        assert_response(response).has_troubleshooting_steps()
        assert_response(response).is_not_too_short(min_words=30)
```

## Test Cases and Fixtures

```python
from evoluteprompt.testing import TestSuite, TestFixture

# Define test fixtures
@TestFixture
class CustomerServiceFixture:
    def setup(self):
        self.provider = OpenAIProvider(
            api_key="YOUR_API_KEY",
            model="gpt-3.5-turbo"
        )
        self.base_prompt = PromptBuilder()\
            .add_system("You are a helpful customer service agent.")\
            .build()
    
    def teardown(self):
        self.provider.close()

# Test suite with multiple cases
class CustomerServiceSuite(TestSuite):
    fixture = CustomerServiceFixture
    
    @TestCase
    def test_response_time(self):
        start_time = time.time()
        response = self.fixture.provider.complete(self.fixture.base_prompt)
        duration = time.time() - start_time
        
        assert duration < 5.0, "Response took too long"
    
    @TestCase(repeat=3)  # Run test multiple times
    def test_consistency(self):
        prompt = self.fixture.base_prompt.add_user("What are your hours?")
        response = self.fixture.provider.complete(prompt)
        
        assert_response(response).is_consistent()
```

## Advanced Testing Features

```python
from evoluteprompt.testing import MockProvider, ResponseValidator

# Mock provider for testing
mock_provider = MockProvider(responses={
    "What are your hours?": "We are open 24/7",
    "How can I reset my password?": "Click the 'Forgot Password' link"
})

# Custom response validator
class CustomerServiceValidator(ResponseValidator):
    def validate_politeness(self, response):
        polite_words = ["please", "thank you", "appreciate"]
        return any(word in response.text.lower() for word in polite_words)
    
    def validate_solution(self, response):
        return (
            "solution" in response.text.lower() or
            "resolve" in response.text.lower()
        )

# Test with custom validator
class AdvancedTest(PromptTest):
    def test_response_quality(self):
        prompt = PromptBuilder()\
            .add_user("I have a problem with my order")\
            .build()
        
        response = self.provider.complete(prompt)
        validator = CustomerServiceValidator()
        
        assert validator.validate_politeness(response)
        assert validator.validate_solution(response)
```

## Performance Testing

```python
from evoluteprompt.testing import PerformanceTest, Metrics

class PromptPerformanceTest(PerformanceTest):
    @TestCase
    def test_response_latency(self):
        self.measure_latency(
            prompt="What is your return policy?",
            max_latency=2.0,
            samples=10
        )
    
    @TestCase
    def test_token_usage(self):
        metrics = Metrics()
        response = self.provider.complete(
            "Explain the warranty process",
            metrics=metrics
        )
        
        assert metrics.token_count < 100
        assert metrics.cost < 0.02  # Maximum cost per request
```

## Integration Testing

```python
from evoluteprompt.testing import IntegrationTest

class WorkflowTest(IntegrationTest):
    def test_customer_support_workflow(self):
        # Test complete workflow
        workflow = CustomerSupportWorkflow()
        
        # Initial greeting
        response = workflow.greet("Hello, I need help")
        assert_response(response).is_greeting()
        
        # Problem identification
        response = workflow.identify_problem("My order is delayed")
        assert_response(response).contains_problem_acknowledgment()
        
        # Solution provision
        response = workflow.provide_solution()
        assert_response(response).has_action_items()
        
        # Satisfaction check
        response = workflow.check_satisfaction("Yes, that helps")
        assert_response(response).is_positive_closure()
``` 