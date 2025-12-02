#!/usr/bin/env python3
"""
Simple test to verify Ollama is working (without MCP).

This tests Ollama directly via the Python library, which is simpler
than testing MCP tools. If this works, Ollama is functioning correctly.
"""

try:
    import ollama
    print("✓ Ollama Python library is installed")
except ImportError:
    print("✗ Ollama Python library not found")
    print("  Install with: pip install ollama")
    exit(1)

print("\n" + "=" * 60)
print("Testing Ollama Connection")
print("=" * 60)
print()

# Test 1: List models
print("1. Testing 'ollama.list()' - List available models...")
try:
    response = ollama.list()
    if hasattr(response, 'models'):
        models = [m.model for m in response.models]
    else:
        models = [m['name'] for m in response.get('models', [])]
    
    if models:
        print(f"   ✓ Success! Found {len(models)} model(s):")
        for model in models[:5]:  # Show first 5
            print(f"      - {model}")
        if len(models) > 5:
            print(f"      ... and {len(models) - 5} more")
    else:
        print("   ⚠ No models found")
        print("   💡 Pull a model: ollama pull llama3")
except Exception as e:
    print(f"   ✗ Error: {e}")
    print("   💡 Make sure Ollama is running: ollama serve")

print()

# Test 2: Check running models
print("2. Testing 'ollama.ps()' - List running models...")
try:
    response = ollama.ps()
    if hasattr(response, 'models'):
        running = [m.name for m in response.models]
    else:
        running = [m['name'] for m in response.get('models', [])]
    
    if running:
        print(f"   ✓ Success! {len(running)} model(s) running:")
        for model in running:
            print(f"      - {model}")
    else:
        print("   ✓ Success! (No models currently running)")
except Exception as e:
    print(f"   ✗ Error: {e}")

print()

# Test 3: Try a simple chat (if we have models)
print("3. Testing 'ollama.chat()' - Simple chat test...")
try:
    # Try to find a model to use
    response = ollama.list()
    if hasattr(response, 'models'):
        available_models = [m.model for m in response.models]
    else:
        available_models = [m['name'] for m in response.get('models', [])]
    
    if available_models:
        # Use first available model
        test_model = available_models[0].split(':')[0]  # Remove tag if present
        print(f"   Using model: {test_model}")
        
        chat_response = ollama.chat(
            model=test_model,
            messages=[{"role": "user", "content": "Say 'Hello, Ollama is working!'"}]
        )
        
        if chat_response and 'message' in chat_response:
            content = chat_response['message']['content']
            print(f"   ✓ Success!")
            print(f"   Response: {content[:100]}...")
        else:
            print("   ⚠ Unexpected response format")
    else:
        print("   ⚠ No models available to test")
        print("   💡 Pull a model: ollama pull llama3")
except Exception as e:
    print(f"   ✗ Error: {e}")
    print("   (This is okay if no models are installed)")

print()
print("=" * 60)
print("Summary")
print("=" * 60)
print()
print("If all tests passed above, Ollama is working correctly!")
print()
print("💡 About MCP Tools:")
print("   The '13 tools enabled' in Ollama Desktop refers to MCP tools")
print("   that allow other applications (like Cursor, Claude Desktop) to")
print("   interact with Ollama via the Model Context Protocol.")
print()
print("   To test MCP tools specifically, run:")
print("     python test_ollama_mcp.py")
print()
print("   Or check your MCP client configuration (Cursor/Claude Desktop)")

