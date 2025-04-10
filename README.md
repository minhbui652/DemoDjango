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
