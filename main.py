from transformers import AutoTokenizer, AutoModelForCausalLM

# Загружаем токенизатор и модель
model_name = "its5Q/rugpt3large_mailqa"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Тест
prompt = "Вопрос: Как быстро тестировать модели с Hugging Face?\nОтвет:"
inputs = tokenizer(prompt, return_tensors="pt")

outputs = model.generate(
    **inputs,
    max_length=200,
    do_sample=True,
    top_k=50,
    top_p=0.95
)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
