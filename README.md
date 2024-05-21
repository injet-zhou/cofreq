## What is cofreq?
cofreq is a tool that make the following api providers compatible with [open-webui](https://github.com/open-webui/open-webui):
- [x] [cohere](https://cohere.com/)
- [x] [groq](https://groq.com/)
- [x] [chatglm](https://chatglm.cn/)
- [x] [qwen](https://tongyi.aliyun.com/)
- [ ] ERNIE

## Getting Started
### Using docker
1. with open-webui
```yaml
services:
  openwebui:
    image: ghcr.io/open-webui/open-webui:ollama
    container_name: openwebui
    ports:
      - 8080:8080
    environment:
      - 'OPENAI_API_BASE_URLS=http://your_ip:7090/api/cohere;http://your_ip:7090/api/groq;http://your_ip:7090/api/chatglm'
      - 'OPENAI_API_KEYS=your_cohere_api_key;your_groq_api_key;your_chatglm_api_key'
    volumes:
      - ./open-webui:/app/backend/data
      - ./ollama:/root/.ollama
    restart: unless-stopped
    depends_on:
      - cofreq

  cofreq:
    image: gorocx/cofreq:latest
    container_name: cofreq
    ports:
      - 7090:7090
    restart: unless-stopped
```

2. with standalone
```bash
docker run -d --name cofreq -p 7090:7090 gorocx/cofreq:latest
```
### Without docker
1. clone the repo
```bash
git clone https://github.com/injet-zhou/cofreq.git
```
2. install dependencies
   create virtual environment(optional)
   
   ```bash
   cd cofreq
   python -m venv venv
   source venv/bin/activate
   ```
   
   install
   
   ```bash
   pip install -r requirements.txt
   ```
   
   

3. run
```bash
pthon main.py
```
