# OnThiDGNL API - Python (Clean Architecture)

Port 1:1 logic của API .NET (C#) sang Python (FastAPI), tổ chức theo Clean Architecture.

## Cấu trúc

```text
back-end-python/
  domain/             # entities thuần
  application/        # DTO, interface repository, use cases
  infrastructure/     # SQL Server repositories, connection
  presentation/       # FastAPI routers, middleware
  main.py             # bootstrap
```

## Phụ thuộc

- `presentation` -> `application`
- `application` -> `domain`
- `infrastructure` implements `application.interfaces`
- `domain` không phụ thuộc layer nào

## Cài đặt / chạy

```bash
cd back-end-python
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Swagger: `http://localhost:8000/docs`

## Đồng bộ Frontend

`front-end/...` đang trỏ tới `http://localhost:8000/api`.
API C# đã được xóa.
