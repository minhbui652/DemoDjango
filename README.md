# DemoDjango
## Model: 
 - Xây dựng model User, Task, Project, Assign, model base
 - Xây dựng các mối quan hệ giữa các model
 - Kết nối model với database (sqlserver)
## Admin:
 - Tạo admin cho các model
 - Thao tác với model trên admin
## View:
 - Sử dụng serializer để chuyển đổi dữ liệu giữa model và json
 - Tạo api CRUD cơ bản cho các model
   - Function base view (FBV) api cho model project
   - Sử dụng APIView cho model task
   - Sử dụng ViewSet cho model assign
## Serializer:
 - Sử dụng serializer để chuyển đổi dữ liệu giữa model và json
 - Tạo serializer cho các model
 - Sử dụng serializer để validate dữ liệu đầu vào
## Authentication:
 - Sử dụng token authentication để xác thực người dùng
## Pagination:
 - Sử dụng pagination để phân trang dữ liệu
## Swagger:
- Sử dụng drf-yasg để test api với swagger
## DATABASE:
- Kết nối database với sqlserver, mysql, sqlite, postgresql
