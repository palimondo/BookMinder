"""End-to-End Tests - Full stack integration tests using subprocess.

E2E tests should:
- Test the complete system from CLI entry point to actual execution
- Use subprocess to invoke the CLI as a real user would
- Verify the entire stack works together correctly
- Be minimal - we only need ONE test to verify wiring
- Use real test fixtures to ensure realistic behavior

Current E2E test:
- cli_wiring_spec.py: Verifies the CLI can successfully invoke the library
  and return formatted output using real Apple Books fixtures
"""
