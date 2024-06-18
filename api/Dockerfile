FROM public.ecr.aws/lambda/python:3.8

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências para o diretório de trabalho
COPY requirements.txt ./
COPY app.py ./

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta em que a aplicação vai rodar
EXPOSE 8080

# Comando para rodar a aplicação
CMD ["app.lambda_handler"]

