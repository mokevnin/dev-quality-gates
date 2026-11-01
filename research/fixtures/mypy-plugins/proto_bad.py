from hello_pb2 import HelloRequest


def make() -> HelloRequest:
    return HelloRequest(name=1)
