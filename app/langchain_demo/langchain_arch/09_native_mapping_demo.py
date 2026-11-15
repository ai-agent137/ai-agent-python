NATIVE_TO_LANGCHAIN_MAPPING = {
    "LLMMessage": "SystemMessage / HumanMessage / AIMessage / ToolMessage",
    "BaseLLMProvider": "ChatModel",
    "PromptService": "ChatPromptTemplate",
    "StructuredOutputService": "OutputParser",
    "ToolDefinition": "Tool / StructuredTool",
    "ToolRegistry": "tools list / 自建 Registry",
    "ToolExecutor": "Agent 工具执行 + 自建权限控制",
    "ChatService": "Chain / Runnable 编排",
    "ToolCallingService": "Agent",
    "RAGService": "Retriever + RAG Chain",
}


def main():
    for native, langchain in NATIVE_TO_LANGCHAIN_MAPPING.items():
        print(f"{native:<30} -> {langchain}")


if __name__ == "__main__":
    main()