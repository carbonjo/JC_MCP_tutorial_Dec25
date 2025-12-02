# OpenAI API Endpoints Explained: Completions vs Chat Completions

## The Error You Encountered

```
Error code: 404 - {'error': {'message': 'This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?', ...}}
```

This error occurs when you try to use the **wrong API endpoint** for a model type.

---

## Two Different API Endpoints

OpenAI provides two main endpoints for text generation:

### 1. **Completions API** (Legacy - `/v1/completions`)
- **Purpose**: Simple text completion (predicting what comes next)
- **Input**: Single text prompt (string)
- **Output**: Completed text
- **Status**: ⚠️ **Deprecated** - Still works but not recommended for new projects
- **Models**: Only works with older models like `text-davinci-003`, `text-curie-001`, etc.

### 2. **Chat Completions API** (Modern - `/v1/chat/completions`)
- **Purpose**: Conversational AI with structured messages
- **Input**: Array of messages with roles (system, user, assistant)
- **Output**: Chat message
- **Status**: ✅ **Recommended** - This is what you should use
- **Models**: Works with all modern models (GPT-4, GPT-3.5-turbo, etc.)

---

## Visual Comparison

### Completions API (Legacy)
```python
# ❌ OLD WAY (Don't use this for modern models)
response = client.completions.create(
    model="gpt-4",  # This will FAIL - gpt-4 is a chat model!
    prompt="Write a poem about AI",
    max_tokens=150
)
text = response.choices[0].text
```

**Why it fails:**
- `gpt-4` is a **chat model**
- Chat models only work with `/v1/chat/completions`
- The Completions API expects older models like `text-davinci-003`

### Chat Completions API (Modern)
```python
# ✅ CORRECT WAY (Use this!)
response = client.chat.completions.create(
    model="gpt-4",  # This works!
    messages=[
        {"role": "user", "content": "Write a poem about AI"}
    ],
    max_tokens=150
)
text = response.choices[0].message.content
```

**Why it works:**
- Uses the correct endpoint for chat models
- Structured message format with roles
- Modern, recommended approach

---

## Key Differences

| Feature | Completions API | Chat Completions API |
|---------|----------------|---------------------|
| **Endpoint** | `/v1/completions` | `/v1/chat/completions` |
| **Input Format** | Single string (`prompt`) | Array of messages (`messages`) |
| **Message Roles** | ❌ No roles | ✅ system, user, assistant |
| **Output Location** | `response.choices[0].text` | `response.choices[0].message.content` |
| **Model Support** | Old models only | All modern models |
| **Status** | Deprecated | ✅ Recommended |
| **Conversation Context** | Limited | ✅ Full conversation history |

---

## When to Use Each

### Use **Chat Completions** (Recommended) ✅
- ✅ **Always** for modern models (GPT-4, GPT-3.5-turbo, etc.)
- ✅ When you need conversation context
- ✅ When you want system prompts
- ✅ For new projects
- ✅ For multi-turn conversations

### Use **Completions** (Legacy) ⚠️
- ⚠️ Only if you're using very old models (`text-davinci-003`, etc.)
- ⚠️ For legacy code that hasn't been updated
- ⚠️ **Not recommended** for new projects

---

## Code Examples

### Example 1: Simple Request

**❌ Wrong (Completions API with chat model):**
```python
response = client.completions.create(
    model="gpt-4",  # Chat model - will fail!
    prompt="Hello, how are you?",
    max_tokens=50
)
```

**✅ Correct (Chat Completions API):**
```python
response = client.chat.completions.create(
    model="gpt-4",  # Chat model - works!
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ],
    max_tokens=50
)
print(response.choices[0].message.content)
```

### Example 2: With System Prompt

**❌ Completions API (no system prompts):**
```python
# Can't set system behavior easily
response = client.completions.create(
    model="text-davinci-003",  # Old model
    prompt="You are a helpful assistant. User: What is Python?",
    max_tokens=100
)
```

**✅ Chat Completions API (with system prompt):**
```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Python?"}
    ],
    max_tokens=100
)
print(response.choices[0].message.content)
```

### Example 3: Multi-Turn Conversation

**❌ Completions API (no conversation history):**
```python
# Each request is independent - no context
response1 = client.completions.create(
    model="text-davinci-003",
    prompt="My name is Alice.",
    max_tokens=10
)
# Next request doesn't know about previous one
response2 = client.completions.create(
    model="text-davinci-003",
    prompt="What's my name?",  # Model doesn't remember!
    max_tokens=10
)
```

**✅ Chat Completions API (full conversation):**
```python
messages = [
    {"role": "user", "content": "My name is Alice."}
]
response1 = client.chat.completions.create(
    model="gpt-4",
    messages=messages
)
# Add assistant's response to history
messages.append({
    "role": "assistant",
    "content": response1.choices[0].message.content
})
# Add new user message
messages.append({"role": "user", "content": "What's my name?"})
# Model remembers the conversation!
response2 = client.chat.completions.create(
    model="gpt-4",
    messages=messages
)
print(response2.choices[0].message.content)  # "Your name is Alice."
```

---

## How to Fix Your Error

### The Problem
You tried to use:
```python
client.completions.create(model="gpt-4", ...)  # ❌ Wrong endpoint
```

### The Solution
Use the Chat Completions API instead:
```python
client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "..."}]
)  # ✅ Correct endpoint
```

---

## Model Compatibility

### Models that work with Completions API:
- `text-davinci-003` (deprecated)
- `text-curie-001` (deprecated)
- `text-babbage-001` (deprecated)
- `text-ada-001` (deprecated)
- ⚠️ **Most of these are deprecated or unavailable**

### Models that work with Chat Completions API:
- ✅ `gpt-4`, `gpt-4-turbo`, `gpt-4o`
- ✅ `gpt-3.5-turbo`
- ✅ `gpt-4o-mini`
- ✅ All modern OpenAI models

**Rule of thumb:** If the model name starts with `gpt-`, use Chat Completions!

---

## In Your MCP Project

Looking at your `mcp_llm_agent.ipynb`, you're already using the **correct** endpoint:

```python
# ✅ This is correct!
response = openai_client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ],
    response_format={"type": "json_object"} if "gpt-4" in model else None
)
```

This is the right way to do it! The error you saw was from the test notebook (`test_openai_api.ipynb`) which demonstrates both APIs for educational purposes.

---

## Summary

1. **The Error**: You tried to use the Completions API (`/v1/completions`) with a chat model (`gpt-4`)
2. **The Solution**: Use Chat Completions API (`/v1/chat/completions`) instead
3. **Key Difference**: 
   - Completions: `prompt="text"` → `response.choices[0].text`
   - Chat: `messages=[...]` → `response.choices[0].message.content`
4. **Best Practice**: Always use Chat Completions for modern models

---

## Quick Reference

```python
# ✅ DO THIS (Chat Completions)
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "Hello!"}
    ]
)
result = response.choices[0].message.content

# ❌ DON'T DO THIS (Completions - deprecated)
response = client.completions.create(
    model="gpt-4",  # Will fail!
    prompt="Hello!",
)
result = response.choices[0].text
```

---

## Further Reading

- [OpenAI Chat Completions API Docs](https://platform.openai.com/docs/api-reference/chat)
- [OpenAI Completions API Docs](https://platform.openai.com/docs/api-reference/completions) (deprecated)
- [Model Endpoints Guide](https://platform.openai.com/docs/models/model-endpoint-compatibility)

