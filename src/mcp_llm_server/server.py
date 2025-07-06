#!/usr/bin/env python3
import asyncio
import subprocess
import json
import logging
from typing import Any

from mcp.server import Server
from mcp.types import Tool, TextContent, Resource
import mcp.server.stdio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMServer:
    def __init__(self):
        self.server = Server("mcp-llm-server")
        self._setup_handlers()
        
    def _setup_handlers(self):
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="claude_prompt",
                    description="Send a prompt to Claude and get a response",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "The prompt to send to Claude"
                            }
                        },
                        "required": ["prompt"]
                    }
                ),
                Tool(
                    name="gemini_prompt",
                    description="Send a prompt to Gemini and get a response",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "The prompt to send to Gemini"
                            }
                        },
                        "required": ["prompt"]
                    }
                ),
                Tool(
                    name="llm_prompt",
                    description="Send a prompt to both Claude and Gemini and get responses",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "prompt": {
                                "type": "string",
                                "description": "The prompt to send to both LLMs"
                            }
                        },
                        "required": ["prompt"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            if name == "claude_prompt":
                response = await self._call_claude(arguments["prompt"])
                return [TextContent(type="text", text=response)]
            
            elif name == "gemini_prompt":
                response = await self._call_gemini(arguments["prompt"])
                return [TextContent(type="text", text=response)]
            
            elif name == "llm_prompt":
                prompt = arguments["prompt"]
                claude_task = asyncio.create_task(self._call_claude(prompt))
                gemini_task = asyncio.create_task(self._call_gemini(prompt))
                
                claude_response, gemini_response = await asyncio.gather(
                    claude_task, gemini_task, return_exceptions=True
                )
                
                response = "## Claude Response:\n"
                if isinstance(claude_response, Exception):
                    response += f"Error: {str(claude_response)}\n"
                else:
                    response += f"{claude_response}\n"
                
                response += "\n## Gemini Response:\n"
                if isinstance(gemini_response, Exception):
                    response += f"Error: {str(gemini_response)}\n"
                else:
                    response += f"{gemini_response}\n"
                
                return [TextContent(type="text", text=response)]
            
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def _call_claude(self, prompt: str) -> str:
        try:
            result = await asyncio.create_subprocess_exec(
                "claude",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await result.communicate(input=prompt.encode())
            
            if result.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                raise Exception(f"Claude CLI error: {error_msg}")
            
            return stdout.decode().strip()
            
        except FileNotFoundError:
            return "Error: claude CLI not found. Please install it first."
        except Exception as e:
            return f"Error calling Claude: {str(e)}"
    
    async def _call_gemini(self, prompt: str) -> str:
        try:
            result = await asyncio.create_subprocess_exec(
                "gemini-cli",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await result.communicate(input=prompt.encode())
            
            if result.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                raise Exception(f"Gemini CLI error: {error_msg}")
            
            return stdout.decode().strip()
            
        except FileNotFoundError:
            return "Error: gemini-cli not found. Please install it first."
        except Exception as e:
            return f"Error calling Gemini: {str(e)}"
    
    async def run(self):
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )

def main():
    server = LLMServer()
    asyncio.run(server.run())

if __name__ == "__main__":
    main()