# DevStore API

API RESTful de e-commerce construída com Django + Django REST Framework, focada em boas práticas de backend, autenticação segura e arquitetura escalável.

---

## 🧠 Sobre o projeto

Este projeto simula o backend completo de uma loja virtual, incluindo:

* Autenticação com JWT
* Carrinho de compras (com suporte a usuários autenticados e anônimos)
* Sistema de pedidos (checkout)
* Controle de estoque
* Documentação automática com Swagger (OpenAPI 3)

O objetivo foi desenvolver uma API seguindo padrões reais de mercado, com foco em organização, validação e consistência.

---

## ⚙️ Tecnologias utilizadas

* Python 3.14.4
* Django
* Django REST Framework
* JWT Authentication
* drf-spectacular (OpenAPI 3 / Swagger)
* SQLite (dev) / PostgreSQL (produção)

---

## 🔐 Autenticação

A API utiliza autenticação via JWT.

### 🔑 Fluxo:

1. Registro de usuário
2. Login → retorna `access_token`
3. Enviar token no header:

```http
Authorization: Bearer <seu_token>
```

---

## 🛒 Funcionalidades principais

### 👤 Usuário

* Registro
* Login com JWT
* Perfil do usuário

### 🛍️ Produtos

* Listagem de produtos
* Detalhes de produto

### 🧺 Carrinho

* Adicionar produto ao carrinho
* Remover produto
* Suporte para usuários não autenticados (session-based)

### 📦 Pedidos (Checkout)

* Criação de pedido a partir do carrinho
* Validação de estoque
* Cálculo de preço total
* Histórico de pedidos

---

## 🔁 Fluxo de compra

1. Usuário adiciona produtos ao carrinho
2. Define endereço
3. Realiza checkout
4. Sistema:

   * valida estoque
   * cria pedido
   * registra itens
   * atualiza estoque

---

## 📄 Documentação da API

A documentação interativa está disponível via Swagger:

```bash
/api/docs/
```

Também é possível acessar o schema OpenAPI:

```bash
/api/schema/
```


---

## 🧪 Como rodar o projeto

### 1. Clonar repositório

```bash
git clone https://github.com/Eletrinho/DevStore.git
cd DevStore
```

---

### 2. Instalar dependências

```bash
uv sync
```

---

### 3. Rodar migrações

```bash
python manage.py migrate
```

---

### 4. Criar superusuário

```bash
python manage.py createsuperuser
```

---

### 5. Rodar servidor

```bash
python manage.py runserver
```

---

## 🚀 Melhorias futuras

* Integração com gateway de pagamento
* Sistema de cupons/descontos
* Cache com Redis
* Deploy em produção com Docker
* Testes automatizados (pytest)

---

---

## ⭐ Contribuição

Sinta-se à vontade para abrir issues ou pull requests.
