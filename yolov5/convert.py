import torch

model = 'models/best'
model.eval()
dummy_input = torch.randn(1, 3, 224, 224)
input_names = ["actual_input"]
output_names = ["output"]
torch.onnx.export(model,
                  dummy_input,
                  "tayo.onnx",
                  verbose=False,
                  input_names=input_names,
                  output_names=output_names,
                  export_params=True,
                  )
