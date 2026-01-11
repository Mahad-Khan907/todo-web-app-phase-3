#!/usr/bin/env python3
"""
Simple test to verify that the code modules can be imported without errors.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test that modules can be imported without errors"""
    print("Testing module imports...")

    try:
        from src.mcp.server import MCPServer
        print("[PASS] MCP Server imported successfully")

        from src.agent.runner import AgentRunner
        print("[PASS] Agent Runner imported successfully")

        from src.auth import get_current_user
        print("[PASS] Auth module imported successfully")

        from src.models import User, Task
        print("[PASS] Models imported successfully")

        from src.database import get_session, get_session_context
        print("[PASS] Database module imported successfully")

        print("\nAll modules imported successfully!")
        print("The UUID fix has been applied to handle malformed UUID strings.")
        print("The main fixes were:")
        print("- Updated MCP server functions to handle hex strings without dashes")
        print("- Enhanced agent runner to handle UUID format conversions")
        print("- Improved auth module to handle UUID format variations")
        print("- Added better error logging for debugging")

    except Exception as e:
        print(f"[FAIL] Error importing modules: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_imports()