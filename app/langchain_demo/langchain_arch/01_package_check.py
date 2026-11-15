from importlib.metadata import version


PACKAGES = [
    "langchain",
    "langchain-core",
    "langchain-openai",
    "langgraph",
]


def main():
    for package in PACKAGES:
        try:
            print(package, "=>", version(package))
        except Exception as exc:
            print(package, "=> 未安装", repr(exc))


if __name__ == "__main__":
    main()