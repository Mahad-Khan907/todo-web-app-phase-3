"""
Test script to verify MCP tools work correctly
"""
import asyncio
from src.mcp.server import MCPServer
from src.agent.runner import AgentRunner
from unittest.mock import Mock, AsyncMock
import uuid


def test_mcp_tools():
    """Test that MCP tools are properly configured"""
    print("Testing MCP Tools...")

    # Create a mock user ID
    user_id = str(uuid.uuid4())

    # Initialize the MCPServer
    server = MCPServer()

    # Test that all required tools exist in the tools dictionary
    tool_names = list(server.tools.keys())

    required_tools = ['add_task', 'list_tasks', 'complete_task', 'update_task', 'delete_task']

    print(f"Available tools: {tool_names}")

    for tool_name in required_tools:
        if tool_name in tool_names:
            print(f"[OK] {tool_name} tool is available")
        else:
            print(f"[FAIL] {tool_name} tool is missing")

    # Test that AgentRunner can be imported
    try:
        from src.agent.runner import AgentRunner
        print("[OK] AgentRunner can be imported successfully")
    except ImportError as e:
        print(f"[FAIL] AgentRunner import failed: {e}")
    except Exception as e:
        print(f"[FAIL] AgentRunner initialization failed: {e}")

    print("\nMCP Tools test completed!")


if __name__ == "__main__":
    test_mcp_tools()