 
pip install grpcio-tools
 
# Generate class
 python -m grpc_tools.protoc -I. --python_out=. schemas/event.proto

