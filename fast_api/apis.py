#
# from fastapi import FastAPI
# from pydantic import BaseModel
#
# app = FastAPI()
# device = "cuda" if torch.cuda.is_available() else "cpu"
#
# class PromptRequest(BaseModel):
#     prompt: str
#     max_tokens: int = 200
#
# @app.post("/generate")
# def generate_endpoint(req: PromptRequest):
#     inputs = tokenizer(req.prompt, return_tensors="pt").to(device)
#     outputs = model.generate(**inputs, max_new_tokens=req.max_tokens)
#     text = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return {"result": text}
#
# # To run locally:
# # uvicorn script_name:app --host 0.0.0.0 --port 8000
