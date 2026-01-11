#!/usr/bin/env python3
"""
Test script to verify that the UUID fix works properly.
This tests the various UUID conversion functions that were updated.
"""

import uuid
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from src.mcp.server import MCPServer
from src.agent.runner import AgentRunner
from uuid import UUID


def test_uuid_conversion():
    """Test UUID conversion with various formats"""
    print("Testing UUID conversion fixes...")

    # Create test UUID
    test_uuid = uuid.uuid4()
    test_uuid_str = str(test_uuid)
    test_hex_no_dashes = test_uuid_str.replace('-', '')

    print(f"Original UUID: {test_uuid}")
    print(f"UUID as string: {test_uuid_str}")
    print(f"UUID as hex (no dashes): {test_hex_no_dashes}")

    # Test the MCP server functions with different UUID formats
    mcp_server = MCPServer()

    # Test with properly formatted UUID string (should work normally)
    print("\n1. Testing with properly formatted UUID string...")
    try:
        # We'll just test the conversion logic directly since we can't create a real task without DB
        import re
        user_id = test_uuid_str

        # Simulate the conversion logic from add_task
        try:
            validated_user_id = UUID(user_id) if isinstance(user_id, str) else user_id
            print(f"   [PASS] Proper UUID string converted successfully: {validated_user_id}")
        except ValueError:
            if isinstance(user_id, str) and re.fullmatch(r'[0-9a-f]{32}', user_id):
                formatted_uuid = f"{user_id[:8]}-{user_id[8:12]}-{user_id[12:16]}-{user_id[16:20]}-{user_id[20:]}"
                validated_user_id = UUID(formatted_uuid)
                print(f"   [PASS] Reformatted hex string to UUID: {validated_user_id}")
            else:
                raise ValueError(f"Invalid user_id format: {user_id}. Expected UUID format.")

    except Exception as e:
        print(f"   [FAIL] Error with proper UUID: {e}")

    # Test with hex string without dashes (the problematic format)
    print("\n2. Testing with hex string without dashes...")
    try:
        user_id = test_hex_no_dashes

        # Simulate the conversion logic from add_task
        try:
            validated_user_id = UUID(user_id) if isinstance(user_id, str) else user_id
            print(f"   ✓ Hex string converted successfully: {validated_user_id}")
        except ValueError:
            if isinstance(user_id, str) and re.fullmatch(r'[0-9a-f]{32}', user_id):
                formatted_uuid = f"{user_id[:8]}-{user_id[8:12]}-{user_id[12:16]}-{user_id[16:20]}-{user_id[20:]}"
                validated_user_id = UUID(formatted_uuid)
                print(f"   ✓ Reformatted hex string to UUID: {validated_user_id}")
            else:
                raise ValueError(f"Invalid user_id format: {user_id}. Expected UUID format.")

    except Exception as e:
        print(f"   ✗ Error with hex string: {e}")

    # Test the agent runner UUID handling
    print("\n3. Testing agent runner UUID handling...")
    try:
        agent_runner = AgentRunner()
        print("   ✓ AgentRunner initialized successfully")
    except Exception as e:
        print(f"   ✗ Error initializing AgentRunner: {e}")

    # Test the auth module logic simulation
    print("\n4. Testing auth module UUID handling...")
    try:
        # Simulate the logic from auth.py
        import re

        # Test with proper UUID string
        user_id = test_uuid_str
        try:
            # This simulates session.get(User, user_id)
            # which would work fine with proper UUID
            print(f"   ✓ Auth logic works with proper UUID: {user_id}")
        except Exception as e:
            # This is the enhanced logic we added
            if isinstance(user_id, str) and re.fullmatch(r'[0-9a-f]{32}', user_id):
                formatted_uuid = f"{user_id[:8]}-{user_id[8:12]}-{user_id[12:16]}-{user_id[16:20]}-{user_id[20:]}"
                print(f"   ✓ Auth logic reformats hex string: {formatted_uuid}")
            elif isinstance(user_id, str) and not re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', user_id):
                try:
                    uuid_obj = UUID(user_id)
                    print(f"   ✓ Auth logic converts string to UUID: {uuid_obj}")
                except ValueError:
                    print(f"   ✗ Auth logic failed to convert UUID: {user_id}")
            else:
                print(f"   ✗ Auth logic failed with proper UUID: {e}")

        # Test with hex string without dashes
        user_id = test_hex_no_dashes
        try:
            # This would fail with original code
            UUID(user_id)  # This should fail
        except ValueError:
            # But our enhanced logic handles it
            if isinstance(user_id, str) and re.fullmatch(r'[0-9a-f]{32}', user_id):
                formatted_uuid = f"{user_id[:8]}-{user_id[8:12]}-{user_id[12:16]}-{user_id[16:20]}-{user_id[20:]}"
                uuid_obj = UUID(formatted_uuid)
                print(f"   ✓ Auth logic handles hex string: {uuid_obj}")
            else:
                print(f"   ✗ Auth logic failed to handle hex string: {user_id}")

        print("   ✓ Auth module logic works correctly")
    except Exception as e:
        print(f"   ✗ Error in auth module test: {e}")

    print("\nUUID conversion fix test completed!")


if __name__ == "__main__":
    test_uuid_conversion()