
from langchain_core.runnables import RunnableLambda


def add_one(x: int) -> int:
    return x + 1
def multiply_two(y: int):
    return y * 2

def main():
    add_one_runable = RunnableLambda(add_one)
    multiply_two_runable = RunnableLambda(multiply_two)
    chain = add_one_runable | multiply_two_runable
    result = chain.invoke(10)
    print(f"result:{result}")

if __name__ == "__main__":
    main()