from hello_pb2 import HelloRequest


def make() -> HelloRequest:
    return HelloRequest(name="a")


def read(req: HelloRequest) -> str:
    return req.name
